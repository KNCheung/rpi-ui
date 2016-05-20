#!/usr/bin/python

from .ScreenBase import ScreenBase
from uuid import uuid1 as uuid

class CPUStatus(ScreenBase):
    """
    1234567890123456
    ================
    CPU  0[--] 1[--]
    ---  2[--] 3[--]
    ================
    """
    def createWidgets(self):
        super(CPUStatus, self).createWidgets()
        self.screen.add_string_widget(uuid(), 'CPU  0[', x=1, y=1)
        self.screen.add_string_widget(uuid(), '] 1[', x=10, y=1)
        self.screen.add_string_widget(uuid(), '2[', x=6, y=2)
        self.screen.add_string_widget(uuid(), '] 3[', x=10, y=2)
        self.screen.add_string_widget(uuid(), ']', x=16, y=1)
        self.screen.add_string_widget(uuid(), ']', x=16, y=2)

        self.cpu = [self.screen.add_hbar_widget(uuid(), x=8, y=1, length=0),
                    self.screen.add_hbar_widget(uuid(), x=14, y=1, length=0),
                    self.screen.add_hbar_widget(uuid(), x=8, y=2, length=0),
                    self.screen.add_hbar_widget(uuid(), x=14, y=2, length=0)]
        
        self.temp = self.screen.add_string_widget(uuid(), '---', x=1, y=2) 
        self.deg = chr(176) 

        self.dataSources['CPUUsage'].attach('CPUStatus', self.updateCPU)
        self.dataSources['CPUTemp'].attach('CPUStatus', self.updateTemp)



    def updateCPU(self, data):
        if self.lcdLock.acquire(False):
            for i in range(4):
                self.cpu[i].set_length(int(round(data[i] / 10.0)))
            self.lcdLock.release() 


    def updateTemp(self, data):
        self.lcdLock.acquire()
        self.temp.set_text("{0:02d}{1}".format(data, self.deg))
        self.lcdLock.release()


