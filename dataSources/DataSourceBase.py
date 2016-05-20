#!/usr/bin/env python3
#encoding: utf8

import logging
log = logging.getLogger()

import threading
import time

def _async(f, name=''):
    tmp = threading.Thread(target=f)
    tmp.setDaemon(True)
    tmp.name += ' ' + name
    tmp.start()

class Timer(threading.Thread):
    def __init__(self):
        super(Timer, self).__init__()
        log.info('create timer')
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
                        _async(target.update, target.__class__.__name__)
                        self._target[target] += target.interval 
            while time.time() > end:
                end += 1

    def attach(self, name, interval): 
        log.info("attach {0} to timer".format(name))
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
        log.info("loading data source {0}".format(self.__class__.__name__))
        self.config = config
        self.timer = timer
        self.occupied = False
        self._observers = {}
        self._data = None
        self.configure()

    def configure(self):
        pass

    def fetch(self):
        raise NotImplementedError

    def get(self):
        return self._data

    def update(self):
        self._data = self.fetch()
        self.notify()

    def notify(self):
        for observer in self._observers.keys():
            _async(lambda : self._observers[observer](self._data), "->{0}".format(observer))

    def start(self):
        self.timer.attach(self, self.interval)

    def stop(self):
        self.timer.detach(self)

    def attach(self, observer, recall):
        log.info("attach {0} to data source {1}".format(observer, self.__class__.__name__))
        self._observers[observer] = recall
        if len(self._observers) == 1:
            self.start()

    def detach(self, observer):
        log.info("detach {0} from data source {1}".format(observer, self.__class__.__name__))
        try:
            del self._observers[observer]
        except KeyError:
            return
        if len(self._observers) == 0:
            self.stop()

