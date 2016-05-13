#!/usr/bin/python

import logging
import threading
import uuid

class ScreenBase(threading.Thread):
    def __init__(self, lcd, lcdLock, config, dataSources):
        threading.Thread.__init__(self)
        logging.debug("loading screen {0}".format(self.__class__.__name__))
        self.lcd = lcd
        self.lcdLock = lcdLock
        self.configFile = config
        self.dataSources = dataSources

        self.name = str(self.__class__.__name__).split('.')[-1]
        self.screen = self.lcd.add_screen(self.name)

        self.createWidgets()

    def config(self, option, default=None):
        try:
            return self.config.get(self.name, option)
        except:
            return default

    def intConfig(self, option, default=0):
        return int(self.config(option, default))

    def floatConfig(self, option, default=0.0):
        return float(self.config(option, default))

    def boolConfig(self, option, default=False):
        tmp = self.config(option, 'False')
        return tmp.lower() in ['1', 'true', 'on']
