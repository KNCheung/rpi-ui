#!/usr/bin/python

from .ScreenBase import ScreenBase
from uuid import uuid1 as uuid

class IPAddr(ScreenBase):
    def createWidgets(self):
        super(IPAddr, self).createWidgets()
        self.screen.add_title_widget(uuid(), "wlan0 addr")
        self.addr = self.screen.add_string_widget(uuid(), "###.###.###.###", 1, 2)
        self.dataSources['Wlan0_IP'].attach('Wlan0_IP', self.update)


    def update(self, data):
        self.lcdLock.acquire()
        self.addr.set_text(data)
        self.lcdLock.release() 

