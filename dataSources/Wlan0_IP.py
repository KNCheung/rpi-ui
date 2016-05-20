#!/usr/bin/env python2
#encoding:utf8

import socket
import fcntl
import struct



import logging
log = logging.getLogger()

from .DataSourceBase import DataSourceBase

class Wlan0_IP(DataSourceBase):
    def configure(self):
        try:
            self.interval = int(self.config.get('Wlan0_IP', 'interval'))
        except Exception as err:
            log.warning("Wlan0_IP's interval not found")
            self.interval = 300

    def fetch(self): 
        log.info("read wlan0 IP address")
        try:
            data = self.get_ip_address('wlan0')
        except :
            log.warning("read IP failed")
            data = '###.###.###.###'
        return data
        
    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl( s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

