#!/usr/bin/python
# -*- coding:utf-8 -*-

from TP_lib import gt1151
from TP_lib import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont
import os
import time


fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
print(fontdir)

epd = epd2in13_V2.EPD_2IN13_V2()
gt = gt1151.GT1151()
GT_Dev = gt1151.GT_Development()
GT_Old = gt1151.GT_Development()

print("init and Clear")
epd.init(epd.FULL_UPDATE)
gt.GT_Init()
epd.Clear(0xFF)

image = Image.new('1', (epd.width, epd.height), 0)
epd.displayPartBaseImage(epd.getbuffer(image))
DrawImage = ImageDraw.Draw(image)
epd.init(epd.PART_UPDATE)

while True:
    print("ok")
    DrawImage.rectangle((0, 20, 200, 34), fill = 1)
    epd.init(epd.PART_UPDATE)
    time.sleep(1)