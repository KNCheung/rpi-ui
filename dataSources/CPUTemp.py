#!/usr/bin/env python2
#encoding:utf8

import logging
log = logging.getLogger()

from .DataSourceBase import DataSourceBase

import subprocess
import re

class CPUTemp(DataSourceBase):
    def configure(self):
        try:
            self.interval = int(self.config.get('CPUTemp', 'interval'))
        except Exception as err:
            self.interval = 5

    def fetch(self): 
        log.info("reading CPU temperature")
        try:
            temp_raw = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf8")
            temp = re.findall(r"[\d\.]+", temp_raw)[0]
        except Exception:
            log.error("unknown error occured")
            return 0
        return int(round(float(temp)))

