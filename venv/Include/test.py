from selenium import webdriver
from selenium.webdriver.firefox import options
from selenium.webdriver.chrome import options
import requests
import queue
import threading
import time
import random
from filedata import *

exitFlag = 0
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("开启线程：" + self.name)
        time.sleep(2)
        process_data(self.name, self.q)
        print ("退出线程：" + self.name)

def process_data(threadName, q):
    while not exitFlag:

        if not workQueue.empty():
            data = q.get()
            port = data.split("*")[1]
            mla_profile_id = data.split("*")[0]
            proxyDict = {
                "http": "http://"+port,
                "https": "https://"+port,
                "ftp": "ftp://10.10.1.10:3128"
            }
            it = 0
            firstipcheckresult = "a"
            while (it != 200 or firstipcheckresult=="a"):
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
                print("%s processing %s is done" % (threadName, data))
                print(workQueue.qsize())
            except:
                try:
                    driver.quit()
                except:
                    print("%s is not even started" % data)
                # queueLock.acquire()
                workQueue.put(data)
                print("%s is reassgned" % data)
                # queueLock.release()


        else:
            print("%s is not release because no task any moew" % threadName)

        time.sleep(1)

threadList = ["Thread-1","Thread-2","Thread-3","Thread-4","Thread-5","Thread-6","Thread-7","Thread-8","Thread-9","Thread-10","Thread-11","Thread-12","Thread-13","Thread-14","Thread-15"]

queueLock = threading.Lock()
workQueue = queue.Queue(100)
threads = []
threadID = 1

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()
#
# # 等待队列清空
# while not workQueue.empty():
#     pass
#
# # 通知线程是时候退出
# exitFlag = 1
#
# # 等待所有线程完成
# for t in threads:
#     t.join()
# print ("退出主线程")
