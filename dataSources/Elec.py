#!/usr/bin/env python
#encoding:utf8

import logging
log = logging.getLogger()

from .DataSourceBase import DataSourceBase

import requests

class Elec(DataSourceBase):
    def configure(self):
        try:
            self.interval = int(self.config.get('Elec', 'interval'))
        except Exception as e:
            log.error(e)
            self.interval = 3600
        try:
            self.area = self.config.get('Elec', 'area', u'韵苑')
            self.building = self.config.get('Elec', 'building', 15)
            self.room = self.config.get('Elec', 'room', 232)
        except:
            self.area = u'韵苑'
            self.building = u'15'
            self.room = u'232'
            log.error(e)

    def fetch(self):
        params = {'area': self.area, 'build': self.building, 'room': self.room}
        try:
            return requests.get("http://campus.hustonline.net/dianfei", params=params, timeout=1)
        except Exception as e:
            log.error(e)

