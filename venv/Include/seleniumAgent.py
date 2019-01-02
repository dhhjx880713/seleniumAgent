from filedata import *
import time
import requests
from selenium import webdriver
import random
import multiprocessing
import os
from utils.tools import get_proxy_dict


class WatchDog(multiprocessing.Process):

    def __init__(self, name):
        super(WatchDog, self).__init__()
        self.name = name

    def scan_port(self):
        pass

    def run(self):
        self.scan_port()

class Worker(multiprocessing.Process):

    def __init__(self, name, url):
        super(Worker, self).__init__()
        self.name = name
        self.task_queue = None
        self.url = url
        self.driver = None

    def set_task_queue(self, job_queue):
        self.task_queue = job_queue

    def run(self):
        print(self.name)
        print(self.pid)
        # self.process_data()
        self.process_data1()

    def process_data1(self):
        print('new job in process pid:', os.getpid())
        self.driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
        self.driver.get(self.url)
        time.sleep(200)

    def process_data(self):
        while True: # pulling the next task off the queue and starting it on the current process.
            task_data = self.task_queue.get()
            self.task_queue.cancel_join_thread()
            print("######################")
            print(self.task_queue.qsize())
            if task_data is None:
                self.task_queue.task_done()
                break
            port = task_data.split("*")[1]
            mla_profile_id = task_data.split("*")[0]
            try:
                print('new job in process pid:', os.getpid())
                ### todo: to be tested
                # mla_url = 'http://127.0.0.1:1204/api/v1/profile/start?automation=true&profileId=' + mla_profile_id
                # resp = requests.get(mla_url)
                # json = resp.json()
                # driver = webdriver.Remote(command_executor=json['value'], desired_capabilities={})
                # driver.get(self.url)
                self.driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')

                self.driver.get(self.url)
                # self.drivers.append(driver)
                time.sleep(230)  ## set watching time
            except:
                pass
            self.task_queue.task_done()

    def stop_process(self):
        # for drive in self.drivers:
        #     print(drive)
        #     drive.quit()
        # print('########################')
        # print(self.driver)
        # self.driver.quit()
        # print(self.driver)
        print('killing process: ', self.name)
        # self.task_queue.cancel_join_thread()
        self.terminate()
        self.join()


class Task(object):

    def __init__(self):
        pass

class SeneliumAgent(object):

    def __init__(self, n_workers=3):
        self.n_workers = n_workers
        self.q_size = 500
        self.proxy_queue = multiprocessing.JoinableQueue(maxsize=self.q_size)
        self.url = r"https://www.youtube.com/watch?v=qXqrEKWPgTI"  ## todo: hard coded url
        self.workers = []
        self.port = ''
        self.previous_ip = ''
        self.current_ip = ''
        self.job_queue = multiprocessing.JoinableQueue()
        ## todo: remove hard coded job_queue
        for i in range(3):
            self.job_queue.put(nameList[i])

    def init_proxy_queue(self):
        for item in nameList:
            self.proxy_queue.put(item)

    def init_connection(self):
        ## fetch the first item from task_queue
        data = self.proxy_queue.get()
        self.port = data.split("*")[1]
        self.proxy_queue.cancel_join_thread()
        connect_state = 0
        previous_check = False
        while connect_state != 200 or not previous_check:
            try:
                resp = requests.get('https://api.ipify.org/', proxies=get_proxy_dict(self.port))
                connect_state = resp.status_code
                self.current_ip = resp.content.decode("utf-8")
                self.previous_ip = self.current_ip
                previous_check = True
            except:
                previous_check = False
        self.proxy_queue.task_done()
        print("initialization succeed. ", self.current_ip)

    def init_watchdog(self):
        pass

    def init_subthreads(self):
        for i in range(self.n_workers):
            self.add_worker("Worker_"+str(i))

    def start_subthreads(self, job_queue):

        for i in range(self.n_workers):
            # self.workers[i].set_task_queue(job_queue)
            self.workers[i].start()

    def stop_subthreads(self):
        for i in range(self.n_workers):
            if self.workers[i].is_alive():
                self.workers[i].stop_process()
        self.workers = []
        # for i in range(self.n_workers):
        #     print(self.workers[i].is_alive())

    def scan_port(self):
        ## scan ports to get new ips, if new ip is different from previous ip, stop and restart subthreads
        previous_check = True
        while True:
            if not self.proxy_queue.empty():

                data = self.proxy_queue.get()
                self.port = data.split("*")[1]
                self.proxy_queue.cancel_join_thread()
                # send request
                try:
                    print(self.port)
                    print(get_proxy_dict(self.port))
                    resp = requests.get('https://api.ipify.org/', proxies=get_proxy_dict(self.port))
                    connect_state = resp.status_code
                    print(connect_state)
                    ## case 1: return valid ip
                    if connect_state == 200:
                        self.current_ip = resp.content.decode("utf-8")
                        print('new ip: ', self.current_ip)
                        if not previous_check:
                            self.stop_subthreads()
                            ## restart subthreads with a new job_queue
                            ## todo: json()
                            time.sleep(0.1)
                            self.init_subthreads()
                            self.start_subthreads(self.job_queue)
                        else:
                            if self.current_ip != self.previous_ip:
                                self.stop_subthreads()
                                ## restart subthreads with a new job_queue
                                time.sleep(0.1)
                                self.init_subthreads()
                                self.start_subthreads(self.job_queue)
                        previous_check = True
                    ## case 2:
                    else:
                        previous_check = False
                except:
                    print("check false ")
                    previous_check = False
                time.sleep(10)

            else:
                break


    def add_worker(self, name):
        new_worker = Worker(name, self.url)
        self.workers.append(new_worker)

    def add_watchdog(self, name):
        return WatchDog(name)

    def run(self):
        self.init_proxy_queue()
        self.init_connection()
        ## todo: initilize job queue
        self.init_subthreads()
        # self.init_watchdog()
        self.start_subthreads(self.job_queue)
        # time.sleep(0.1)
        # self.stop_subthreads()
        self.scan_port()
        # self.init_subthreads()
        # self.start_subthreads(self.job_queue)


if __name__ == "__main__":
    agent = SeneliumAgent()
    # agent.init_proxy_queue()
    # agent.init_connection()
    agent.run()
    # print(agent.task_queue.qsize())