#!/usr/bin/env python3
#encoding:utf8

from daemon import Daemon
import time

class Main(Daemon):
    def __init__(self):
        super().__init__(pidfile='/tmp/rpi-ui.pid')

    def run(self):
        while True:
            time.sleep(100)

