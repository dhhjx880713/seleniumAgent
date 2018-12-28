import time
import requests
from selenium import webdriver
import random


def process_data(threadName, q, exitFlag):
    while not exitFlag:

        if not q.empty():
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
                print(q.qsize())
            except:
                try:
                    driver.quit()
                except:
                    print("%s is not even started" % data)
                # queueLock.acquire()
                q.put(data)
                print("%s is reassgned" % data)
                # queueLock.release()


        else:
            print("%s is not release because no task any moew" % threadName)

        time.sleep(1)