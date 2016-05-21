#!/usr/bin/python

import logging
log = logging.getLogger()

import threading
import uuid

class ScreenBase(threading.Thread):
    def __init__(self, lcd, lcdLock, config, dataSources):
        threading.Thread.__init__(self)
        log.info("loading screen {0}".format(self.__class__.__name__))
        self.lcd = lcd
        self.lcdLock = lcdLock
        self.config = config
        self.dataSources = dataSources

        self.name = str(self.__class__.__name__).split('.')[-1]
        self.screen = self.lcd.add_screen(self.name)

        self.createWidgets()

    def setBacklight(self, state):
        self.screen.set_backlight(state)

    def createWidgets(self):
        self.screen.set_heartbeat('off')
        try:
            self.duration = int(self.config.get(self.name, 'duration'))
        except Exception as e:
            log.warning("{0}'s duration not found".format(self.name))
            log.error(e)
            self.duration = 5
        self.screen.set_duration(self.duration)

    def configGet(self, option, default=None):
        try:
            return self.config.get(self.name, option)
        except:
            return default

    def intConfigGet(self, option, default=0):
        return int(self.configGet(option, default))

    def floatConfigGet(self, option, default=0.0):
        return float(self.configGet(option, default))

    def boolConfigGet(self, option, default=False):
        tmp = self.configGet(option, 'False')
        return tmp.lower() in ['1', 'true', 'on']
