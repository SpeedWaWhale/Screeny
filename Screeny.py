#!/usr/bin/python
# -*- coding:utf-8 -*-

from TP_lib import gt1151
from TP_lib import epd2in13_V2

epd = epd2in13_V2.EPD_2IN13_V2()
gt = gt1151.GT1151()

def clear_screen():
    print("init and Clear")
    epd.init(epd.FULL_UPDATE)
    gt.GT_Init()
    epd.Clear(0xFF)

def sleep_screen():
    epd.sleep()

def stop_screen():
    epd.Dev_exit()

clear_screen()
sleep_screen()