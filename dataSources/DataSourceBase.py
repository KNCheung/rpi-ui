#!/usr/bin/env python3
#encoding: utf8

import logging
import threading
import time

def _async(f):
    tmp = threading.Thread(target=f)
    tmp.setDaemon(True)
    tmp.start()

class Timer(threading.Thread):
    def __init__(self):
        super(Timer, self).__init__()
        logging.debug('create timer')
        self._target = {}
        self.setDaemon(True)
        self.lock = threading.Lock()

    def run(self):
        end = time.time() + 1
        while True:
            try:
                time.sleep(end - time.time()) 
            except IOError:
                pass
            else:
                t = time.time()
                for target in self._target.keys():
                    if t >= self._target[target]:
                        _async(target.update)
                        self._target[target] += target.interval

            while time.time() > end:
                end += 1

    def attach(self, name, interval): 
        logging.debug("attach {0} to timer".format(name))
        _async(name.update)
        self.lock.acquire()
        self._target[name] = interval + time.time()
        self.lock.release()
    
    def detach(self, name): 
        self.lock.acquire()
        try:
            del self._target[name]
        except KeyError:
            pass
        self.lock.release()



class DataSourceBase(object):
    def __init__(self, config, timer):
        logging.debug("loading data source {0}".format(self.__class__.__name__))
        self.config = config
        self.timer = timer
        self.occupied = False
        self._observers = {}
        self._data = None

    def fetch(self):
        raise NotImplementedError

    def get(self):
        return self._data

    def update(self):
        logging.debug("update data source {0}".format(self.__class__.__name__))
        self._data = self.fetch()
        self.notify()

    def notify(self):
        for observer in self._observers.keys():
            _async(lambda : self._observers[observer](self._data))

    def start(self):
        self.timer.attach(self, self.interval)

    def stop(self):
        self.timer.detach(self)

    def attach(self, observer, recall):
        logging.debug("attach {0} to data source {1}".format(observer, self.__class__.__name__))
        self._observers[observer] = recall
        if len(self._observers) == 1:
            self.start()

    def detach(self, observer):
        logging.debug("detach {0} from data source {1}".format(observer, self.__class__.__name__))
        try:
            del self._observers[observer]
        except KeyError:
            return
        if len(self._observers) == 0:
            self.stop()

