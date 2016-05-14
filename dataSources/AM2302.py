#!/usr/bin/env python2
#encoding:utf8

import logging

from .DataSourceBase import DataSourceBase

import Adafruit_DHT as dht

class AM2302(DataSourceBase):
    def configure(self):
        try:
            self.interval = int(self.config.get('AM2302', 'interval'))
        except Exception as err:
            self.interval = 60
        try:
            self.pin = int(self.config.get('AM2302', 'pin'))
        except Exception as err:
            self.pin = 17

    def fetch(self): 
        logging.debug("Start reading AM2302")
        try:
            h, t = dht.read_retry(dht.AM2302, self.pin, retries=4, delay_seconds=5)
        except RuntimeError:
            h, t = (None, None)
        try:
            logging.debug("AM2302: h={0}, t={1}".format(int(h), int(t)))
        except Exception:
            logging.error("failed to read AM2302")
        return (h, t)
        
