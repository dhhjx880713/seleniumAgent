import multiprocessing
import time
from selenium import webdriver
import os
exit = False
import threading
import signal


class Worker(multiprocessing.Process):

    def __init__(self, name, url):
        super(Worker, self).__init__()
        self.name = name
        self.task_queue = None
        self.url = url
        # self.driver = None
        self.shutdown_flag = multiprocessing.Event()
        self.play_time = 200

    def set_task_queue(self, job_queue):
        self.task_queue = job_queue

    def run(self):
        print(self.name)
        print(self.pid)
        # self.process_data()
        self.process_data1()

    def process_data1(self):
        print('new job in process pid:', os.getpid())
        driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
        driver.get(self.url)
        past_time = 0
        time_clip = 0.1
        while not self.shutdown_flag.is_set() and past_time <= self.play_time:

            past_time +=time_clip
            time.sleep(time_clip)
        driver.quit()

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
        self.shutdown_flag.set()
        time.sleep(0.1)
        self.terminate()
        self.join()


class Worker1(threading.Thread):

    def __init__(self, name, url):
        super(Worker1, self).__init__()
        self.name = name
        self.task_queue = None
        self.url = url
        # self.driver = None
        self.shutdown_flag = threading.Event()
        self.play_time = 200

    def set_task_queue(self, job_queue):
        self.task_queue = job_queue

    def run(self):
        print(self.name)
        print(self.ident)
        # self.process_data()
        self.process_data1()

    def process_data1(self):
        print('new job in process pid:', os.getpid())
        driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
        driver.get(self.url)
        past_time = 0
        time_clip = 0.1
        while not self.shutdown_flag.is_set() and past_time <= self.play_time:
            past_time +=time_clip
            time.sleep(time_clip)
        # driver.quit()

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
        self.shutdown_flag.set()
        # self.terminate()
        self.join()


def hang():
    while True:
        # print('hanging..')
        # time.sleep(1)
        driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
        driver.get("https://www.youtube.com/watch?v=qXqrEKWPgTI")
        time.sleep(100)


class Job(threading.Thread):

    def __init__(self):
        super(Job, self).__init__()
        self.shutdown_flag = threading.Event()
        self.testflag = multiprocessing.Event()

    def run(self):
        print('Thread #%s started' % self.ident)
        driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
        driver.get("https://www.youtube.com/watch?v=qXqrEKWPgTI")
        while not self.shutdown_flag.is_set():
            # ... Job code here ...
            time.sleep(0.1)

        # ... Clean shutdown code here ...
        print('Thread #%s stopped' % self.ident)
        driver.quit()


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


def event_exit_test():
    new_job = Job()
    new_job.start()
    time.sleep(10)
    new_job.shutdown_flag.set()

def main():
    # p = multiprocessing.Process(target=hang)
    # p.start()
    # time.sleep(10)
    # p.terminate()
    # p.join()
    # print('main process exiting..')

    url = "https://www.youtube.com/watch?v=qXqrEKWPgTI"
    new_worker1 = Worker('new worker1', url)
    new_worker1.start()
    time.sleep(5)
    new_worker1.stop_process()

    # new_worker2 = Worker('new worker2', url)
    # new_worker1.start()
    # new_worker2.start()

    # event_exit_test()



if __name__ == '__main__':
    main()