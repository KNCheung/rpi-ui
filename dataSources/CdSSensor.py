#!/usr/bin/env python

import logging
log = logging.getLogger()

from .DataSourceBase import DataSourceBase 

import RPi.GPIO as GPIO
import time
import os

DEBUG = 1
GPIO.setmode(GPIO.BCM)

class CdSSensor(DataSourceBase):
    def configure(self):
        try:
            self.interval = int(self.config.get('CdSSensor', 'interval'))
        except Exception as err:
            self.interval = 60
        try:
            self.RCpin = int(self.config.get('CdSSensor', 'pin'))
        except Exception as err:
            self.RCpin = 23

    def fetch(self):
        log.debug("start reading CdS Sensor")
        return self.RCtime()

    def RCtime(self):
        GPIO.setup(self.RCpin, GPIO.OUT)
        GPIO.output(self.RCpin, GPIO.LOW)
        time.sleep(0.005)
        
        GPIO.setup(self.RCpin, GPIO.IN)
        ts = time.time()
        while (GPIO.input(self.RCpin) == GPIO.LOW):
            time.sleep(0.001)
        return time.time() -ts

