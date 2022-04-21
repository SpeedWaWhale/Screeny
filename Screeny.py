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
    epd.init(epd.FULL_UPDATE)
    gt.GT_Init()
    epd.Clear(0xFF)

def draw_text():
    font15 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)
    canvas = Image.new('RGB',(122,125), "black")
    epd.displayPartBaseImage(epd.getbuffer(canvas))
    DrawImage = ImageDraw.Draw(canvas)

def sleep_screen():
    epd.sleep()

def stop_screen():
    epd.Dev_exit()

#clear_screen()
draw_text()
#sleep_screen()