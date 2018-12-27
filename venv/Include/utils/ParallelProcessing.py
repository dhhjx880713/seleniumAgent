# -*- coding: utf-8 -*-

import multiprocessing as mp
from multiprocessing import Process, Queue, Manager, Lock, Pool
from multiprocessing.managers import BaseManager
from multiprocessing import current_process
import os
import sys

PROCESS_EVENT_DEBUG_OUTPUT = 0
PROCESS_EVENT_ANIMATION_LOADED = 1
PROCESS_EVENT_SET_CONSTRAINTS = 2
PROCESS_EVENT_CLEAR_CONSTRAINTS =3
PROCESS_EVENT_GENERATE_MOTION = 4
PROCESS_EVENT_SET_SCENE_CONFIGURATION = 5
PROCESS_EVENT_SYNCHRONIZE_SCENE = 6

class SharedMemoryManager(BaseManager):
    pass


queue = Queue()
def getQueue():
    return queue

lock = Lock()
def getLock():
    return lock

SharedMemoryManager.register("getQueue", callable=getQueue) 
SharedMemoryManager.register("getLock", callable=getLock)  


class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.mgr = mp.Manager()
        self.active = self.mgr.list()
        self.lock = mp.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
    def __str__(self):
        with self.lock:
            return str(self.active)


class ProcessEvent(object):
    def __init__(self):
        self.type = 0
        self.value = 0
                    

globalLock = Lock()


class GlobalProcessPool():
    globalPool = None
    def create(self,processes):
        self.__class__.globalPool = Pool(processes)
        
    def stop(self):
        if  self.__class__.globalPool != None:
            self.__class__.globalPool.close()
            self.__class__.globalPool.join()
            
    def get(self):
        return self.__class__.globalPool
    
    
class GlobalEventQueue():
    queue = None
    def set(self,queue):
        self.__class__.globalPool = queue
            
    def get(self):
        return self.__class__.queue
    

class Context(object):
    """ note this is not a shared object and can only be used from the main process to pass the shared objects to processes
    """
    def __init__(self):
        self.sharedObjectManager = None
        self.processEventHandlerThread = None
        self.processPool = None
        self.eventQueue = None
        self.processLock = None

    def init(self,createProcessPool= True):
        """  singleton constructor """
        self.sharedObjectManager = SharedMemoryManager()
        self.sharedObjectManager.start()
        #properties = self.sharedObjectManager.getGlobalConfig().getProperties()
        #print(properties)
        config = None
        if config is not None and "numberOfProcesses"in config.keys():
            numberOfProcesses = int(config["numberOfProcesses"])
        else:
            print("config not found")
            numberOfProcesses = 6

        self.eventQueue =  self.sharedObjectManager.getQueue()
        self.processLock = self.sharedObjectManager.getLock()

        if createProcessPool and numberOfProcesses >0:
            self.processPool = Pool(numberOfProcesses)
        
    def test(self):
        self.eventQueue.put("the queue works")
        event = self.eventQueue.get()
        print((str(event)))
        self.lock()
        self.eventQueue.put("the lock works")
        event = self.eventQueue.get()
        self.unlock()
        print((str(event)))
        
    def deinit(self):
        if self.processEventHandlerThread != None:
            self.processEventHandlerThread.keepRunning = False
        if self.processPool != None:
            self.processPool.close()
            self.processPool.join()
        if  self.sharedObjectManager != None:
            self.sharedObjectManager.shutdown()

    def getSharedMemoryManager(self):
        return self.sharedObjectManager

    def getProcessEventHandlerThread(self):
        return self.processEventHandlerThread
    
    def getProcessPool(self):
        return self.processPool
     
    def getEventQueue(self):
        return self.eventQueue
    
    def getLock(self):
        return self.processLock
    
    #only works from the main process
    def lock(self):
        self.processLock.acquire()
    
    #only works from the main process  
    def unlock(self):
        self.processLock.release()


class ThreadSaveList():
    def __init__(self):
        self.list =[]
        self.lock = Lock()
            
    def addItem(self,newitem):#):
        self.lock.acquire()
        self.list.append(newitem)
        self.lock.release()    
        
            
    def getItem(self,index):#):
        self.lock.acquire()
        if index> -1 and index < len(self.list):
            item = self.list[index]
            self.lock.release()
            return item
        else:
            self.lock.release()
            return None
    
    def getLength(self):#
        self.lock.acquire()
        num = len(self.list)
        self.lock.release()
        return num

    def getList(self):
       self.lock.acquire()
       return self.animations
       self.lock.release()


def savePrint(message):
    print(str(os.getpid()) +": "+  message)
    

global globalContext
globalContext =Context()





