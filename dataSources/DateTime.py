#!/usr/bin/env python2
#encoding:utf8

from .DataSourceBase import DataSourceBase
from datetime import datetime

class DateTime(DataSourceBase):
    def configure(self):
        try:
            self.interval = int(self.config.get('DateTime', 'interval'))
        except:
            self.interval = 1

    def fetch(self):
        return datetime.now()

