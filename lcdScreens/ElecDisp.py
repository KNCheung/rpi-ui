#!/usr/bin/python

import logging
log = logging.getLogger()

from .ScreenBase import ScreenBase
from uuid import uuid1 as uuid

class ElecDisp(ScreenBase):
    def createWidgets(self):
        super(ElecDisp, self).createWidgets()
        self.screen.add_title_widget(uuid(), "Electricity")
        self.elec = self.screen.add_string_widget(uuid(), "############", 1, 2)
        self.dataSources['Elec'].attach('ElecDisp', self.update)


    def update(self, data):
        if data.status_code == 200:
            d = data.json()
            if d['code'] == 200:
                remain = float(d['data']['remain'])
                recent = d['data']['recent']
                date = recent.keys()
                date.sort(reverse=True)
                last = float(recent[date[1]]['dianfei'])
                delta = remain - last
                self.lcdLock.acquire()
                self.elec.set_text(' {0:0.1f}   {1:0.1f}'.format(delta, remain))
                self.lcdLock.release() 
        else:
            log.warning(data.status_code)

