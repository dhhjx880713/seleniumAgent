from filedata import *
import time
import requests
from selenium import webdriver
import random
import multiprocessing
import threading
import os
from utils.tools import get_proxy_dict
import urllib
import json

class WatchDog(multiprocessing.Process):

    def __init__(self, name):
        super(WatchDog, self).__init__()
        self.name = name

    def scan_port(self):
        pass

    def run(self):
        self.scan_port()

class Worker(multiprocessing.Process):

    def __init__(self, name, tasks=None):
        super(Worker, self).__init__()
        self.name = name
        self.task_queue = None
        self.tasks = tasks
        self.shutdown_flag = multiprocessing.Event()
        self.play_time = 180

    def set_task_queue(self, job_queue):
        self.task_queue = job_queue

    def run(self):
        print(self.name)
        print(self.pid)
        self.process_data()

    def process_data(self):
        # if
        print('new job in process pid:', os.getpid())
        driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
        for task in self.tasks:
            if task is not None:
                try:
                    driver.get(task['url'])
                    past_time = 0
                    time_clip = 0.1
                    while not self.shutdown_flag.is_set() and past_time <= task['watchingtime'] * 60:
                        past_time +=time_clip
                        time.sleep(time_clip)
                except:
                    print("selenium open url failed")
            else:
                continue
            if self.shutdown_flag.is_set():
                break
        driver.quit()

    # def process_data_old(self):
    #     while True: # pulling the next task off the queue and starting it on the current process.
    #         task_data = self.task_queue.get()
    #         self.task_queue.cancel_join_thread()
    #         print("######################")
    #         print(self.task_queue.qsize())
    #         if task_data is None:
    #             self.task_queue.task_done()
    #             break
    #         port = task_data.split("*")[1]
    #         mla_profile_id = task_data.split("*")[0]
    #         try:
    #             print('new job in process pid:', os.getpid())
    #             ### todo: to be tested
    #             # mla_url = 'http://127.0.0.1:1204/api/v1/profile/start?automation=true&profileId=' + mla_profile_id
    #             # resp = requests.get(mla_url)
    #             # json = resp.json()
    #             # driver = webdriver.Remote(command_executor=json['value'], desired_capabilities={})
    #             # driver.get(self.url)
    #             self.driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
    #
    #             self.driver.get(self.url)
    #             # self.drivers.append(driver)
    #             time.sleep(230)  ## set watching time
    #         except:
    #             pass
    #         self.task_queue.task_done()

    def stop_process(self):
        print('killing process: ', self.name)
        # self.task_queue.cancel_join_thread()
        self.shutdown_flag.set()
        time.sleep(0.2)
        self.terminate()
        self.join()


class Task(object):

    def __init__(self):
        pass

class SeneliumAgent(object):

    def __init__(self, n_workers=3, port=None, rest_server_address=None, timeout=5, debug=False):
        self.n_workers = n_workers
        # self.q_size = 500
        # self.proxy_queue = multiprocessing.JoinableQueue(maxsize=self.q_size)
        # self.url = r"https://www.google.com/"  ## todo: hard coded url
        self.workers = []
        self.port = port
        self.previous_ip = ''
        self.current_ip = ''
        self.timeout = timeout
        self.debug = debug
        self.rest_server_address = rest_server_address
        # self.job_queue = multiprocessing.JoinableQueue()
        # ## todo: remove hard coded job_queue
        # for i in range(3):
        #     self.job_queue.put(nameList[i])

    # def init_proxy_queue(self):
    #     for item in nameList:
    #         self.proxy_queue.put(item)
    #     print("proxy queue initialized! ")

    def init_connection(self):
        ## fetch the first item from task_queue
        # data = self.proxy_queue.get()
        # data = r'31e7f927-07b3-481e-919f-a4eed6b22336*195.154.161.119:4376'
        # self.port = data.split("*")[1]
        if self.debug:
            print(self.port)
        # self.proxy_queue.cancel_join_thread()
        connect_state = 0
        previous_check = False
        while connect_state != 200 or not previous_check:
            try:
                resp = requests.get('http://api.ipify.org/', proxies=get_proxy_dict(self.port), timeout=self.timeout)
                connect_state = resp.status_code
                self.current_ip = resp.content.decode("utf-8")
                self.previous_ip = self.current_ip
                previous_check = True
            except:
                previous_check = False
                print("check failed")
                ## todo: add expection handle
                continue
        # self.proxy_queue.task_done()
        if self.debug:
            print("initialization succeed. ", self.current_ip)

    def init_watchdog(self):
        pass

    def init_subthreads(self, task_list):
        assert len(task_list) == self.n_workers
        self.workers = []
        for i in range(self.n_workers):
            if task_list[i] is not None:
                print("add worker_"+str(i))
                self.add_worker("Worker_"+str(i), task_list[i])

    def start_subthreads(self):

        for i in range(self.n_workers):
            self.workers[i].start()

    def stop_subthreads(self):
        if self.workers != []:
            for worker in self.workers:
                if worker.is_alive():
                    worker.stop_process()
                self.workers = []  ## clean workers pool

    def restart_task(self):
        print("restart tasks")
        ## stop previous subthreads
        self.stop_subthreads()
        # print(r"46.101.125.90:8080/schedule/3/" + self.port[-4:])
        if self.rest_server_address.endswith('/'):
            self.rest_server_address = self.rest_server_address[:-1]
        request_url = '/'.join([self.rest_server_address, str(self.n_workers), str(self.port[-4:])])
        # print(request_url)
        new_resp = requests.get(request_url,
                                auth=('admin', 'password'), timeout=5)
        task_list = json.loads(new_resp.content.decode("utf-8"))
        # print(task_list)
        # print(json_data)

        ## restart subthreads with a new job_queue
        time.sleep(0.1)
        self.init_subthreads(task_list)
        self.start_subthreads()


    def scan_port(self):
        ## scan ports to get new ips, if new ip is different from previous ip, stop and restart subthreads
        previous_check = True
        while True:
            try:
                if self.debug:
                    print(self.port)
                    print(get_proxy_dict(self.port))

                resp = requests.get('http://api.ipify.org/', proxies=get_proxy_dict(self.port), timeout=self.timeout)
                connect_state = resp.status_code
                if self.debug:
                    print(resp.content.decode("utf-8"))
                    print(connect_state)
                ## case 1: return valid ip
                if connect_state == 200:
                    self.previous_ip = self.current_ip
                    self.current_ip = resp.content.decode("utf-8")
                    # print('new ip: ', self.current_ip)
                    if not previous_check:
                        self.restart_task()
                    else:
                        if self.current_ip != self.previous_ip:
                            if self.debug:
                                print("ip address changed! ")
                            self.restart_task()
                    previous_check = True
                ## case 2:
                else:
                    previous_check = False
            except:
                print("non response!")

            time.sleep(15)


    def add_worker(self, name, tasks):
        new_worker = Worker(name, tasks=tasks)
        self.workers.append(new_worker)

    def add_watchdog(self, name):
        return WatchDog(name)

    def run(self):
        # self.init_proxy_queue()
        self.init_connection()
        ## todo: initilize job queue
        # self.init_subthreads()
        # self.init_watchdog()
        # self.start_subthreads(self.job_queue)
        # time.sleep(0.1)
        # self.stop_subthreads()
        self.scan_port()
        # self.init_subthreads()
        # self.start_subthreads(self.job_queue)


if __name__ == "__main__":
    rest_server_address = r'http://46.101.125.90:8080/schedule/'
    port = nameList[-3].split("*")[1]
    timeout = 15
    resend_time = 15
    agent = SeneliumAgent(port=port, rest_server_address=rest_server_address, timeout=timeout, debug=True)
    agent.run()
