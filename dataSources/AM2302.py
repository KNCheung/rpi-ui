#!/usr/bin/env python2
#encoding:utf8

import logging

from .DataSourceBase import DataSourceBase

import Adafruit_DHT as dht

class AM2302(DataSourceBase):
    interval = 60
    def fetch(self): 
        try:
            h, t = dht.read_retry(dht.AM2302, 17, retries=5, delay_seconds=5)
        except RuntimeError:
            h, t = (None, None)
        return (h, t)
        
