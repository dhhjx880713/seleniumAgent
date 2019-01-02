from multiprocessing import Process
import time

def task():
    time.sleep(5)

procs = []

for x in range(2):
    proc = Process(target=task)
    procs.append(proc)
    proc.start()

time.sleep(2)

# for proc in procs:
#     proc.join(timeout=0)
#     if proc.is_alive():
#         print("Job is not finished!")