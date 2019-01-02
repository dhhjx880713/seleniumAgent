from multiprocessing import Process, Lock, Pool
import os
import multiprocessing
import time
import sys


def f(l, i):
    l.acquire()
    print('hello world', i)
    l.release()

def f_nolock(i):
    print('hellp world', i)

def demo_lock_process():
    lock = Lock()

    for num in range(10):
        # Process(target=f, args=(lock, num)).start()
        Process(target=f_nolock, args=(num,)).start()


def f1(x):
    return x * x

def demo_pool_workers():
    pool = Pool(processes=4)
    for i in pool.imap_unordered(f1, range(10)):
        print(i)
    # evaluate "f(20)" asynchronously
    res = pool.apply_async(f1, (20,))      # runs in *only* one process
    print(res.get(timeout=10))              # prints "400"
    # pool.apply_async
    # launching multiple evaluations asynchronously *may* use more processes
    multiple_results = [pool.apply_async(os.getpid, ()) for i in range(40)]
    print([res.get(timeout=1) for res in multiple_results])


def daemon():
    print('Starting:', multiprocessing.current_process().name)
    time.sleep(20)
    print('Exiting :', multiprocessing.current_process().name)

def non_daemon():
    print('Starting:', multiprocessing.current_process().name)
    print('Exiting :', multiprocessing.current_process().name)


def waiting_for_processes():
    d = multiprocessing.Process(name='daemon', target=daemon)
    d.daemon = True

    n = multiprocessing.Process(name='non-daemon', target=non_daemon)
    n.daemon = False

    d.start()
    time.sleep(1)
    n.start()

    d.join()
    print('d.is_alive()', d.is_alive())
    n.join()


def f2(x):
    # time.sleep(10)
    print(multiprocessing.current_process().pid)
    # print()
    return x * x

def print_all_processes_id():
    p = multiprocessing.Pool(6)
    # print(p.apply_async(f2, args=(range(6))))
    print(p.map(f2, range(6)))


if __name__ == '__main__':
    # demo_lock_process()
    # demo_pool_workers()
    # waiting_for_processes()
    print_all_processes_id()