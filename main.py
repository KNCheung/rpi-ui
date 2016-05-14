#!/usr/bin/env python3
#encoding:utf8

import sys, os
import threading

import logging
log = logging.getLogger()

from daemon import Daemon
import time

try: 
    import configparser
except:
    import ConfigParser as configparser

from lcdScreens import screens
from lcdproc.server import Server

from dataSources import dataSources, Timer

class Main(Daemon):
    def __init__(self, configureFile):
        super(Main, self).__init__(pidfile='/tmp/rpi-ui.pid')

        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        self.config = configparser.SafeConfigParser()
        self.config.read(configureFile) 

    def loadDataSources(self):
        log.info("start loading data sources")
        self.timer = Timer()
        self.timer.name = 'Timer'
        self.dataSources = {}
        for ds in dataSources.keys():
            self.dataSources[ds] = dataSources[ds](self.config, self.timer)


    def loadScreens(self):
        log.info("start loading screens")
        self.pool = []
        self.lcd = Server(debug=False)
        self.lcd.start_session()
        self.lcdLock = threading.Lock()
        for scr in self.config.sections():
            if screens.has_key(scr) and self.config.has_option(scr, 'active') and self.config.getboolean(scr, 'active'):
                self.pool.append(screens[scr](self.lcd, self.lcdLock, self.config, self.dataSources))

    def run(self):
        self.loadDataSources()
        self.loadScreens()

        self.timer.start()
        while True:
            time.sleep(15)
            log.info("heartbeat. num of threads={0}".format(threading.active_count()))

