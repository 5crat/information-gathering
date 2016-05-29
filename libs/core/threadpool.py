#!/usr/bin/env python
# -*-coding:utf-8-*-
# -*-author:scrat-*-


from Queue import Queue
from Queue import Empty
from threading import Thread
from threading import ThreadError

class Worker(Thread):
    def __init__(self, threadPool, **kargs):
        Thread.__init__(self)
        self.threadPool = threadPool
        self.setDaemon(True)
        self.state = None
        self.start()

    def run(self):
        while True:
            if self.state == 'STOP':
                break
            try:
                func, args, kargs = self.threadPool.workQueue.get()
            except Empty:
                break
            try:
                res = func(*args, **kargs)
                self.threadPool.resultQueue.put(res)
                self.threadPool.workDone()
            except:
                break
        def stop(self):
            self.state = 'STOP'


class ThreadPool(object):
    """
    ThreadPool
    """
    def __init__(self, threadNum):
        """
        init thread pool
        :param threadNum:
        :return:
        """
        self.workQueue = Queue()
        self.resultQueue = Queue()
        self.threadPool = []
        self.threadNum = threadNum

    def startThreads(self):
        """
        start thread
        :return:
        """
        for i in range(self.threadNum):
            self.threadPool.append(Worker(self))

    def workJoin(self, *args, **kargs):
        """
        wait thread finish
        :param args:
        :param kargs:
        :return:
        """
        self.workQueue.join()

    def addJob(self, func, *args, **kargs):
        """
        add job
        :param func:
        :param args:
        :param kargs:
        :return:
        """
        self.workQueue.put((func, args, kargs))

    def workDone(self, *args):
        """
        work done
        :param args:
        :return:
        """
        self.workQueue.task_done()

    def getResult(self, *args, **kargs):
        """
        get result
        :param args:
        :param kargs:
        :return:
        """
        return self.resultQueue.get(*args, **kargs)

    def stopThreads(self):
        """
        stop thread
        :return:
        """
        for thread in self.threadPool:
            #thread.join()
            thread.stop()
        del self.threadPool[:]
