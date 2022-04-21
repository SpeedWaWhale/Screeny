#!/usr/bin/python
# -*- coding:utf-8 -*-

from TP_lib import gt1151
from TP_lib import epd2in13_V2

epd = epd2in13_V2.EPD_2IN13_V2()
gt = gt1151.GT1151()
GT_Dev = gt1151.GT_Development()
GT_Old = gt1151.GT_Development()

print("init and Clear")
epd.init(epd.FULL_UPDATE)
gt.GT_Init()
epd.Clear(0xFF)