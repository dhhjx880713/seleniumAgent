import multiprocessing
from time import sleep
import time
import random
from selenium import webdriver
import os


def init(queue):
    global idx
    idx = queue.get()

def f(x):
    global idx
    process = multiprocessing.current_process()
    sleep(1)
    return (idx, process.pid, x * x)

def test():
    ids = [0, 1, 2, 3]
    manager = multiprocessing.Manager()
    idQueue = manager.Queue()

    for i in ids:
        idQueue.put(i)

    p = multiprocessing.Pool(8, init, (idQueue,))
    print(p.map(f, range(8)))


def task1(x):
    print(multiprocessing.current_process().pid)
    sleep(1)
    return x **2


def test1():
    p = multiprocessing.Pool(processes=8)
    print(p.map(task1, range(8)))


urllocaton = [
    "https://youtu.be/bFBjdTfsxv0",
    "https://youtu.be/bFBjdTfsxv0",
    "https://youtu.be/bFBjdTfsxv0",
    "https://youtu.be/bFBjdTfsxv0"
]

def task2(url):
    print('new job in process pid:', os.getpid())
    driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
    driver.get(url)
    # time.sleep(230)


def test2():
    p = multiprocessing.Pool(processes=4)
    p.map(task2, urllocaton)
    # time.sleep(5)
    # p.close()
    # p.join()

def run(idx, i):
    time.sleep(random.random() * i)
    print(idx, ':', i)


def run_jobs(jobs, workers=1):
    q = multiprocessing.Queue()
    def worker(idx):
        try:
            while True:
                args = q.get(timeout=1)
                run(idx, *args)
        except q.empty:
            return

    for job in jobs:
        q.put(job)

    processes = []
    for i in range(0, workers):
        p = multiprocessing.Process(target=worker, args=[i])
        p.daemon = True
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    # test1()
    # run_jobs([('job', i) for i in range(0, 10)], workers=5)
    test2()