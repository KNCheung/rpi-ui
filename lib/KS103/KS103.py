#!/usr/bin/env python
#coding:utf8

import wiringpi as wpi
import time

class KS103(object):
    def __init__(self, addr = 0x75):
        self.addr = addr
        self.fd = wpi.wiringPiI2CSetup(addr)
        self.cmd(0xc1)
        self.cmd(0xc3)
        self.cmd(0x73)

    def cmd(self, code):
        if wpi.wiringPiI2CWriteReg8(self.fd, 0x02, code):
            raise IOError("I2C write ERROR {0:x}@{1:x}".format(self.addr, code))

    def read8(self, addr=0x02):
        return wpi.wiringPiI2CReadReg8(self.fd, addr)

    def read16(self):
        return (self.read8(0x02) << 8) | (self.read8(0x03))

    def getDistance(self):
        self.cmd(0xb4)
        time.sleep(0.1)
        return self.read16()

    def getIntensity(self):
        self.cmd(0xa0)
        time.sleep(0.05)
        return self.read16()

    def getTemperature(self):
        self.cmd(0xc9)
        time.sleep(0.2)
        return self.read16() / 16.0


if __name__ == '__main__':
    p = KS103()
    while True:
        print("Intensity: {0}".format(p.getIntensity()))
        print("Temperature: {0}".format(p.getTemperature()))
        print("Distance: {0}mm".format(p.getDistance()))
        time.sleep(1)

