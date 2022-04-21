#!/usr/bin/python
# -*- coding:utf-8 -*-

from TP_lib import gt1151
from TP_lib import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont
import os
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
print(fontdir)
epd = epd2in13_V2.EPD_2IN13_V2()
gt = gt1151.GT1151()

def clear_screen():
    print("init and Clear")
    # epd.init(epd.FULL_UPDATE)
    # gt.GT_Init()
    #epd.Clear(0xFF)

def draw_text():
    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 10, 200, 34), fill = 0)

def sleep_screen():
    epd.sleep()

def stop_screen():
    epd.Dev_exit()

clear_screen()
draw_text()
#sleep_screen()