import threading
import queue
from filedata import *
import time
import requests
from selenium import webdriver
import random


class Thread(threading.Thread):

    def __init__(self, threadID, name, q):
        super(Thread, self).__init__()
        self.name = name
        self.threadID = threadID
        self.q = q
        self.exitFlag = 0

    def run(self, exitFlag=0):
        print("Starting " + self.name)
        self.process_data()
        print("Exiting " + self.name)

    def process_data(self):
        while not self.exitFlag:
            if not self.q.empty():
                data = self.q.get()
                port = data.split("*")[1]
                mla_profile_id = data.split("*")[0]
                proxyDict = {
                    "http": "http://" + port,
                    "https": "https://" + port,
                    "ftp": "ftp://10.10.1.10:3128"
                }
                it = 0
                firstipcheckresult = "a"
                while (it != 200 or firstipcheckresult == "a"):
                    time.sleep(5)
                    try:
                        firstipcheck = requests.get('https://api.ipify.org/', proxies=proxyDict)
                        it = firstipcheck.status_code
                        firstipcheckresult = firstipcheck.content
                        print(firstipcheckresult)
                    except:
                        time.sleep(5)
                        print("check false ")
                time.sleep(5)
                it = 0
                secondcheckresult = firstipcheckresult
                while (it != 200 or firstipcheckresult == secondcheckresult):
                    time.sleep(10)
                    try:
                        secondipcheck = requests.get('http://api.ipify.org/', proxies=proxyDict)
                        it = secondipcheck.status_code
                        secondcheckresult = secondipcheck.content
                        print(secondcheckresult)
                    except:
                        print("check false 2 ")
                        time.sleep(5)

                print("Start")
                try:
                    mla_url = 'http://127.0.0.1:1204/api/v1/profile/start?automation=true&profileId=' + mla_profile_id
                    resp = requests.get(mla_url)
                    json = resp.json()
                    print(json)
                    driver = webdriver.Remote(command_executor=json['value'], desired_capabilities={})
                    urllocaton = [
                        "https://www.youtube.com/watch?v=qXqrEKWPgTI",
                        "https://www.youtube.com/watch?v=_Sai8fN1FhU",
                        "https://www.youtube.com/watch?v=U-4d9qAKT9c",
                        "https://www.youtube.com/watch?v=yBr_8JCsQVE",
                        "https://www.youtube.com/watch?v=Ks0VhM_gFG8",
                    ]
                    driver.get(urllocaton[random.randint(0, 4)])
                    time.sleep(5)
                    # driver.get('https://www.youtube.com/watch?v=rxZezeqKJrM')
                    time.sleep(230)
                    driver.get(urllocaton[random.randint(0, 4)])
                    time.sleep(230)
                    driver.close()
                    try:
                        driver.quit()
                    except:
                        print("force quit failed")
                    print("%s processing %s is done" % (self.name, data))
                    print(self.q.qsize())
                except:
                    try:
                        driver.quit()
                    except:
                        print("%s is not even started" % data)
                    # queueLock.acquire()
                    self.q.put(data)
                    print("%s is reassgned" % data)
                    # queueLock.release()


            else:
                print("%s is not release because no task any moew" % self.name)

            time.sleep(1)

    def exit(self):
        self.exitFlag = 1


class SenuliumAgnet(object):

    def __init__(self, n_thread=3, port=None, profileID=None):
        self.n_thread = n_thread
        self.port = port
        self.profileID = profileID
        self.subthreads = []
        self.subthread_ID = 1
        self.q_size = 100
        self.queueLock = threading.Lock()
        self.work_queue = queue.Queue(self.q_size)


    def init_work_queue(self):
        self.queueLock.acquire()
        for work in nameList:
            self.work_queue.put(work)
        self.queueLock.release()
        print("queue is initialized")

    def add_subthread(self, thread_name):
        new_thread = Thread(self.subthread_ID, thread_name, self.work_queue)
        self.subthread_ID += 1
        self.subthreads.append(new_thread)

    def run(self):
        ## initialize all subthreads
        for i in range(1, self.n_thread+1):
            self.add_subthread("Thread-" + str(i))
            self.subthreads[i-1].start()
        self.init_work_queue()
        if self.work_queue.empty():
            self.stop_subthreads()
        for thread in self.subthreads:
            thread.join()

    def stop_subthreads(self):
        for thread in self.subthreads:
            thread.exit()


if __name__ == "__main__":
    agent = SenuliumAgnet()
    agent.run()