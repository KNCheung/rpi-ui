#!/usr/bin/env python2
#encoding:utf8

import logging
log = logging.getLogger()

from .DataSourceBase import DataSourceBase

import psutil

class CPUUsage(DataSourceBase):
    def configure(self):
        try:
            self.interval = int(self.config.get('CPUUsage', 'interval'))
        except Exception as err:
            self.interval = 5

    def fetch(self): 
        return psutil.cpu_percent(percpu=True)
        
