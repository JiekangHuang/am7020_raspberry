#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sim7020_modem.py
# @Author : Zack Huang ()
# @Link   : zack@atticedu.com
# @Date   : 2020/11/5 下午1:40:47

import serial
from time import time, sleep
from gpiozero import LED

GSM_OK = "OK\r\n"
GSM_ERROR = "ERROR\r\n"


class SIM7020Modem:
    def __init__(self, port, baudrate, reset_pin):
        self._at = serial.Serial(port, baudrate, timeout=0.05)
        self._reset_pin = LED(reset_pin)

    def restart(self):
        self._reset_pin.off()
        sleep(0.5)
        self._reset_pin.on()
        sleep(5)

    def testAT(self, timeout_s=10):
        startTime = time()
        while(time() - startTime < timeout_s):
            self.sendAT()
            if(self.waitResponse(0.2) == 1):
                return True
            sleep(0.1)
        return False

    def streamWrite(self, *args):
        cmd = ""
        for arg in args:
            cmd += str(arg)
        cmd = bytes(cmd, 'utf-8')
        self._at.write(cmd)

    def sendAT(self, *args):
        cmd = "AT"
        for arg in args:
            cmd += str(arg)
        cmd = bytes(cmd + "\r\n", 'utf-8')
        self._at.write(cmd)

    def streamRead(self):
        self._at.read()

    def streamGetLength(self, numChars, timeout_s=1):
        startTime = time()
        data = ""
        while(time() - startTime < timeout_s):
            data += self._at.read(numChars).decode("utf-8")
            if(data != "" and len(data) == numChars):
                return data

    def streamGetIntBefore(self, lastChar, timeout_s=1):
        startTime = time()
        data = ""
        while(time() - startTime < timeout_s):
            data += self._at.read().decode("utf-8")
            if(data != "" and data.endswith(lastChar)):
                return int(data[:-1])
        return -9999

    def streamGetStringBefore(self, lastChar, timeout_s=1):
        startTime = time()
        data = ""
        while(time() - startTime < timeout_s):
            data += self._at.read().decode("utf-8")
            if(data != "" and data.endswith(lastChar)):
                return data[:-1]
        return ""

    def streamSkipUntil(self, c, timeout_s=1):
        startTime = time()
        while(time() - startTime < timeout_s):
            ch = self._at.read().decode("utf-8")
            if(ch == c):
                return True
        return False

    def waitResponse(self, timeout_s=1, r1=GSM_OK, r2=GSM_ERROR, r3=None, r4=None, r5=None):
        index = 0
        startTime = time()
        data = ""
        while(time()-startTime < timeout_s):
            c = self._at.read().decode("utf-8")
            data += c
            # if(c):
                # print(c, end="")

            if(r1 and data.endswith(r1)):
                index = 1
                break
            elif(r2 and data.endswith(r2)):
                index = 2
                break
            elif(r3 and data.endswith(r3)):
                index = 3
                break
            elif(r4 and data.endswith(r4)):
                index = 4
                break
            elif(r5 and data.endswith(r5)):
                index = 5
                break
        return index

    def ParseSubMsg():
        pass
