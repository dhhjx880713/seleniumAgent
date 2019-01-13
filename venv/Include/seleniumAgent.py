from filedata import *
import time
import requests
from selenium import webdriver
import random
import multiprocessing
import os
from utils.tools import get_proxy_dict
import json
from selenium.common.exceptions import NoSuchElementException
IGNORED_EXCEPTIONS = (NoSuchElementException,)



class WatchDog(multiprocessing.Process):

    def __init__(self, name):
        super(WatchDog, self).__init__()
        self.name = name

    def scan_port(self):
        pass

    def run(self):
        self.scan_port()

class Worker(multiprocessing.Process):

    def __init__(self, name, tasks=None, debug=False):
        super(Worker, self).__init__()
        self.name = name
        self.tasks = tasks
        self.shutdown_flag = multiprocessing.Event()
        self.debug = debug

    def run(self):
        print(self.name)
        print(self.pid)
        self.process_youtube()

    def process_youtube(self):
        print('new job in process pid:', os.getpid())
        driver = webdriver.Chrome(executable_path=r'../../geckodriver-v0.23.0-win64/geckodriver.exe')
        for task in self.tasks:
            if task is not None:
                end_time = time.time() + task['watchingtime'] * 60  ## minutes to seconds
                try:
                    driver.get(task['url'])
                    time_clip = 0.1
                    while not self.shutdown_flag.is_set() and time.time() < end_time:
                        player_state = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
                        '''
                        youtube player_state
                        Player_state = 0 means end
                        Player_state = 1 means playing
                        Player_state = -1 means advertise

                        '''
                        if player_state == -1:
                            if self.debug:
                                print("ad is playing")
                            try:
                                skip_button = driver.find_element_by_class_name('ytp-ad-skip-button')
                                if skip_button:
                                    print("find skip button, prepare click in 5 seconds")
                                    time.sleep(task['ad_watchingtime'])
                                    while True:
                                        try:
                                            skip_button.click()
                                            break
                                        except:
                                            time.sleep(0.1)
                            except NoSuchElementException:
                                print('no skip button!')
                        elif player_state > 0: ### normal playing state

                            time.sleep(time_clip) ### continue to play
                        elif player_state == 0: ## for a very short video
                            break
                        else:
                            pass
                except IGNORED_EXCEPTIONS:
                    print("selenium open url failed")
            else:
                continue
            if self.shutdown_flag.is_set():
                print('break now:', os.getpid())
                break
        driver.quit()

    def stop_process(self):
        print('killing process: ', self.name)
        # self.task_queue.cancel_join_thread()
        self.shutdown_flag.set()
        time.sleep(0.8)
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
        new_worker = Worker(name, tasks=tasks, )
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
