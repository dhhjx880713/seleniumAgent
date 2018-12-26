import requests
import time
import queue
from selenium import webdriver
import random
import threading


nameList1 = [
            "31e7f927-07b3-481e-919f-a4eed6b22336*195.154.161.119:4376",
            "70064960-883f-4366-8278-46dc00860408*195.154.161.119:4377",
            "1fbfc13c-3104-4d01-a897-8606cbeed2c9*195.154.161.119:4378",
            "c2e7ee41-7746-4a03-a76a-7158b930fe10*195.154.161.119:4379",
            "247d0202-b266-49c9-b39d-9bbddbe868f7*195.154.161.119:4380",
            "5438a69b-4ede-4ea9-9aa4-3d1c2df2cd0e*195.154.161.119:4381",
            "227e402a-532f-43b9-85c9-297f6a6422a5*195.154.161.119:4382",
            "7ca1d0ce-2e62-4250-9fac-00aa5c5aa170*195.154.161.119:4383",
            "22995334-8a15-4f8a-835a-44a62ea498c5*195.154.161.119:4384",
            "261b0917-8083-4a60-9ae3-b0439324ec29*195.154.161.119:4385",
            "ecf5c1b3-a66a-4c0a-863e-d53c8cbaa1d4*195.154.161.119:4386",
            "5f629784-0737-4758-95e2-e8d0653b6a67*195.154.161.119:4387",
            "7dc3b2cb-aa61-4e41-87b8-f5bd0c263c19*195.154.161.119:4388",
            "d3ae333a-0768-4329-8964-b04390686669*195.154.161.119:4389",
            "86376e87-eb83-4b4c-bf9c-08bb4af6a043*195.154.161.119:4390",
            "b560f237-a20c-4740-99ed-30bf5988e519*195.154.161.119:4391",
            "242ac39b-0215-4451-b419-052d92be47ed*195.154.161.119:4392",
            "49f7b219-e8fc-4d86-a2d9-f04c01a945f0*195.154.161.119:4393",
            "c17d5c55-dff1-40df-b7bb-85fb4277c903*195.154.161.119:4394",
            "81bf11aa-d93d-476b-9423-b93f8c394208*195.154.161.119:4395",
            "27c06b79-cade-4d05-8f04-1a12050a114b*195.154.161.119:4396",
            "9d630c66-d61b-49e0-a273-dea31938fc48*195.154.161.119:4397",
            "a92484cc-8a18-497e-bed4-2e99f8018a2c*195.154.161.119:4398",
            "ebb620ad-ce94-4372-8c3a-b411c962baf8*195.154.161.119:4399",
            "7b64e224-9bf1-4dad-ae01-cc3b938c88e3*195.154.161.119:4400",
            "a78b2947-e0bd-487f-bf0c-ce042d6dc673*195.154.161.119:4376",
            "ef794dde-daad-439d-9758-bc70e7b5b4ac*195.154.161.119:4377",
            "bffbc919-c5d2-42e4-8724-1de9872a41bc*195.154.161.119:4378",
            "1a2d23c1-a300-4cd4-9f2f-b23e01f6d167*195.154.161.119:4379",
            "b4f0e101-81d1-4683-8e89-fecb48bdac50*195.154.161.119:4380",
            "1e1a117a-788d-4e90-b95b-cfa5d3ed68d6*195.154.161.119:4381",
            "f1b82437-01a0-4b89-8df5-89df8edff98f*195.154.161.119:4382",
            "97c7c308-5051-41e8-936e-306dbf3fd247*195.154.161.119:4383",
            "f24c4ac4-312f-4f6d-8ea5-7091b36356b4*195.154.161.119:4384",
            "2b64063e-301a-4fae-8a96-58bcaf8d26e8*195.154.161.119:4385",
            "c1ebe8a3-ffea-4a83-91da-41da63542569*195.154.161.119:4386",
            "5ffe1f84-c16e-42bd-8f0a-0132da8152cf*195.154.161.119:4387",
            "9bde2718-12f1-458b-a229-56c75770d8ab*195.154.161.119:4388",
            "5abf17eb-dcda-4689-8ce2-7d8c42940f50*195.154.161.119:4389",
            "21ef11ad-c0e6-485f-955e-943abeea9e25*195.154.161.119:4390",
            "f86f83c9-cc7b-4405-bbee-787ef7d8f70d*195.154.161.119:4391",
            "9a885162-7705-4902-97f9-8192dd051d08*195.154.161.119:4392",
            "790fc65f-4007-45aa-ba73-934be38f007c*195.154.161.119:4393",
            "41c8bed0-bb66-4b9a-a47f-8577258b5f1c*195.154.161.119:4394",
            "6d64bc2f-66b6-4728-9e81-d6f6142ebfe9*195.154.161.119:4395",
            "904a22b4-bd45-4456-b873-c58a74e878fa*195.154.161.119:4396",
            "203efa23-f439-4343-b26e-fd1312b39afc*195.154.161.119:4397",
            "bffdf9cb-e025-4e85-95c8-220917777cf1*195.154.161.119:4398",
            "a9f9024e-70d6-4ef9-b3d3-151570033f58*195.154.161.119:4399",
            "d2c2ccac-3034-421b-a63b-f238cbc84687*195.154.161.119:4400",
            "c364f563-cf91-4200-8236-01e6a1f48c41*195.154.161.119:4376",
            "cb9029f6-fb63-464a-b422-1d2384698c48*195.154.161.119:4377",
            "4ce549db-22b7-437f-bc86-c157574520c2*195.154.161.119:4378",
            "ca628a05-7f95-477a-a8db-4d609f71957a*195.154.161.119:4379",
            "f1ef1724-f9e2-4609-a9f6-eade40ee7e7b*195.154.161.119:4380",
            "22d2b04b-6605-43bb-bcf3-fe280021fba5*195.154.161.119:4381",
            "68c9b5d5-16eb-40d5-9fdf-1d7f33f6ca74*195.154.161.119:4382",
            "e293c285-ffa3-49ef-beaf-35a400dc16c2*195.154.161.119:4383",
            "014fae9d-8bea-4ad3-bf44-31ecbb19f486*195.154.161.119:4384",
            "3e5981b1-31e0-4482-aacc-1479e31768a9*195.154.161.119:4385",
            "41e0e77a-4780-4b8a-8162-316ad0d5af35*195.154.161.119:4386",
            "df3a89ab-1b89-49cd-9441-711241b0210c*195.154.161.119:4387",
            "88786e53-bf77-4227-9c80-f78dd9e2b2fb*195.154.161.119:4388",
            "b395dad3-42a5-44d7-a48a-2224a85ef105*195.154.161.119:4389",
            "6481a5c2-68cb-4eef-983a-8e542a00636c*195.154.161.119:4390",
            "ba907c17-d02a-4d82-8557-0ddbc410c2e3*195.154.161.119:4391",
            "c6bbdb7d-1e1e-48bb-abb0-a8deeba6ea37*195.154.161.119:4392",
            "9d320aae-b800-42a5-8184-c1e068245e92*195.154.161.119:4393",
            "7010f54b-ef51-400f-a803-71467ed01a62*195.154.161.119:4394",
            "858dfdcc-295a-4072-8578-967529fc98c5*195.154.161.119:4395",
            "f998574c-8373-47d0-ad96-dafc8cc63470*195.154.161.119:4396",
            "9d88db0a-ef86-4e3c-be20-a82bc815329e*195.154.161.119:4397",
            "ddb6d675-af71-4f68-889c-b4ec4ba60b21*195.154.161.119:4398",
            "7b64e224-9bf1-4dad-ae01-cc3b938c88e3*195.154.161.119:4399",
            "7fe40e96-3a04-4c5c-aa63-42d4f5d48bdb*195.154.161.119:4400",
            "87cf5284-6985-4a9b-87ce-69b16d8a37bb*195.154.161.119:4400",
            ]


def test():
    data = "ecf5c1b3-a66a-4c0a-863e-d53c8cbaa1d4*195.154.161.119:4386";
    port = data.split("*")[1]
    # print(port)
    proxyDict = {
        "http": "http://" + port,
        "https": "https://" + port,
        "ftp": "ftp://10.10.1.10:3128"
    }
    # firstipcheck = requests.get('https://api.ipify.org/', proxies=proxyDict)
    firstipcheck = requests.get('https://api.ipify.org/')
    # print(type(firstipcheck))

    # print(firstipcheck.content)
    # print(firstipcheck.status_code)
    # ipaddres = firstipcheck.content.decode("utf-8")
    # print(ipaddres)

    # json_data = firstipcheck.json()
    # print(json_data)

    mla_profile_id = data.split("*")[0]
    mla_url = 'http://127.0.0.1:1204/api/v1/profile/start?automation=true&profileId=' + mla_profile_id
    resp = requests.get(mla_url)
    print(resp.json())


exitFlag = 0


def process_data_test():
    while not exitFlag:
        data = "ecf5c1b3-a66a-4c0a-863e-d53c8cbaa1d4*195.154.161.119:4386";
        port = data.split("*")[1]
        mla_profile_id = data.split("*")[0]
        proxyDict = {
            "http": "http://" + port,
            "https": "https://" + port,
            "ftp": "ftp://10.10.1.10:3128"
        }
        status_code = 0
        firstipcheckresult = "a"
        while (status_code != 200 or firstipcheckresult == "a"):
            time.sleep(5)
            try:
                # firstipcheck = requests.get('https://api.ipify.org/', proxies=proxyDict)
                firstipcheck = requests.get('https://api.ipify.org/')
                status_code = firstipcheck.status_code
                print(status_code)
                firstipcheckresult = firstipcheck.content
                print(firstipcheckresult)
            except:
                time.sleep(5)
                print("check false ")


workQueue = queue.Queue(100)


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

queueLock = threading.Lock()
def test_process_data():
    thread_name = r'testThread'
    process_data(thread_name, workQueue)
    for word in nameList1:
        workQueue.put(word)


if __name__ == "__main__":
    test()
    # process_data()