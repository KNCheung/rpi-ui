#!/usr/bin/python

from ScreenBase import ScreenBase
import psutil, subprocess, re
from time import sleep
from uuid import uuid1 as uuid

class CPUStatus(ScreenBase):
    """
    1234567890123456
    ================
    CPU  0[--] 1[--]
    ---  2[--] 3[--]
    ================
    """
    def getCPUTemp(self):
        temp_raw = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf8")
        temp = re.findall(r"[\d\.]+", temp_raw)[0]
        return int(round(float(temp)))

    def run(self):
        self.screen.add_string_widget(uuid(), 'CPU  0[', x=1, y=1)
        self.screen.add_string_widget(uuid(), '] 1[', x=10, y=1)
        self.screen.add_string_widget(uuid(), '2[', x=6, y=2)
        self.screen.add_string_widget(uuid(), '] 3[', x=10, y=2)
        self.screen.add_string_widget(uuid(), ']', x=16, y=1)
        self.screen.add_string_widget(uuid(), ']', x=16, y=2)

        cpu = [self.screen.add_hbar_widget(uuid(), x=8, y=1, length=0),
               self.screen.add_hbar_widget(uuid(), x=14, y=1, length=0),
               self.screen.add_hbar_widget(uuid(), x=8, y=2, length=0),
               self.screen.add_hbar_widget(uuid(), x=14, y=2, length=0)]
        
        temp = self.screen.add_string_widget(uuid(), '---', x=1, y=2)

        deg = chr(176)

        while True:
            temp.set_text('{0:02d}{1}'.format(self.getCPUTemp(), deg))
            for _ in range(10):
                status = psutil.cpu_percent(percpu=True)
                for i in range(4):
                    cpu[i].set_length(int(round(status[i] / 10.0)))
                sleep(0.5)
