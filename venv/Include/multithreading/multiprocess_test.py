import multiprocessing
import time


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, startTimes, name=None):
        multiprocessing.Process.__init__(self)
        if name:
            self.name = name
        print('created process: {0}'.format(self.name))
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.startTimes = startTimes

    def stopProcess(self):
        elapseTime = time.time() - self.startTimes[self.name]
        print('killing process {0} {1}'.format(self.name, elapseTime))
        self.task_queue.cancel_join_thread()
        self.terminate()
        # now want to get the process to start procesing another job

    def run(self):
        '''
        The process subclass calls this on a separate process.
        '''
        proc_name = self.name
        print(proc_name)
        print(self.pid)
        while True:
            # pulling the next task off the queue and starting it
            # on the current process.
            task = self.task_queue.get()
            self.task_queue.cancel_join_thread()

            if task is None:
                # Poison pill means shutdown
                # print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            self.startTimes[proc_name] = time.time()
            answer = task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    def __init__(self, a, b, startTimes):
        self.a = a
        self.b = b
        self.startTimes = startTimes
        self.taskName = 'taskName_{0}_{1}'.format(self.a, self.b)

    def __call__(self):
        import time
        import os

        print('new job in process pid:', os.getpid(), self.taskName)

        if self.a == 2:
            time.sleep(20000)  # simulate a hung process
        else:
            time.sleep(3)  # pretend to take some time to do the work
        return '%s * %s = %s' % (self.a, self.b, self.a * self.b)

    def __str__(self):
        return '%s * %s' % (self.a, self.b)


if __name__ == '__main__':
    # Establish communication queues
    # tasks = this is the work queue and results is for results or completed work
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # parentPipe, childPipe = multiprocess.Pipe(duplex=True)
    mgr = multiprocessing.Manager()
    startTimes = mgr.dict()

    # Start consumers
    numberOfProcesses = 4
    processObjs = []
    for processNumber in range(numberOfProcesses):
        processObj = Consumer(tasks, results, startTimes)
        processObjs.append(processObj)

    for process in processObjs:
        process.start()

    # Enqueue jobs
    num_jobs = 30
    for i in range(num_jobs):
        tasks.put(Task(i, i + 1, startTimes))

    # Add a poison pill for each process object
    for i in range(numberOfProcesses):
        tasks.put(None)

    # process monitor loop,
    killProcesses = {}
    executing = True
    while executing:
        allDead = True
        for process in processObjs:
            name = process.name
            # status = consumer.status.getStatusString()
            status = process.is_alive()
            pid = process.ident
            elapsedTime = 0
            if name in startTimes:
                elapsedTime = time.time() - startTimes[name]
            if elapsedTime > 10:
                process.stopProcess()

            print("{0} - {1} - {2} - {3}".format(name, status, pid, elapsedTime))
            if allDead and status:
                allDead = False
        if allDead:
            executing = False
        time.sleep(3)

    # Wait for all of the tasks to finish
    # tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1