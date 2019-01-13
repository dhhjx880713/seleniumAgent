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
from selenium_op import SelenuimOP
IGNORED_EXCEPTIONS = (NoSuchElementException,)


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
        self.process_data()

    def process_data(self):
        print('new job in process pid:', os.getpid())
        for task in self.tasks:
            if self.debug:
                print(task)
            if task is not None:
                youtube_op = SelenuimOP(driver_type='Firefox', debug=self.debug)
                youtube_op.youtube_click(task, self.shutdown_flag)
            else:
                continue
            if self.shutdown_flag.is_set():
                print('break now:', os.getpid())
                break

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
        self.workers = []
        self.port = port
        self.previous_ip = ''
        self.current_ip = ''
        self.timeout = timeout
        self.debug = debug
        self.rest_server_address = rest_server_address

    def init_connection(self):
        if self.debug:
            print(self.port)
        connect_state = 0
        previous_check = False
        while connect_state != 200 or not previous_check:
            try:
                resp = requests.get('http://api.ipify.org/', proxies=get_proxy_dict(self.port), timeout=self.timeout)
                connect_state = resp.status_code
                self.current_ip = resp.content.decode("utf-8")
                self.previous_ip = self.current_ip
                previous_check = True
            except IGNORED_EXCEPTIONS:
                previous_check = False
                print("check failed")
                continue
        if self.debug:
            print("initialization succeed. ", self.current_ip)

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
        '''
        when ip address is changed, restart all processes
        :return:
        '''
        print("restart tasks")
        ## stop previous subthreads
        self.stop_subthreads()
        if self.rest_server_address.endswith('/'):
            self.rest_server_address = self.rest_server_address[:-1]
        request_url = '/'.join([self.rest_server_address, str(self.n_workers), str(self.port[-4:])])
        if self.debug:
            print(request_url)
        new_resp = requests.get(request_url,
                                auth=('admin', 'password'), timeout=5)
        task_list = json.loads(new_resp.content.decode("utf-8"))
        '''
        task_list: list of task
        keys of each task:
        keys:
            url,
            platform
            watchingtime
            ad_watchingtime
            profileID
            type
        '''

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

    def run(self):
        self.init_connection()
        self.scan_port()


if __name__ == "__main__":
    rest_server_address = r'http://46.101.125.90:8080/schedule/'
    port = nameList[-3].split("*")[1]
    timeout = 15
    resend_time = 15
    agent = SeneliumAgent(port=port, rest_server_address=rest_server_address, timeout=timeout, debug=True)
    agent.run()
