#!/usr/bin/python
# -*- coding:utf-8 -*-

from TP_lib import gt1151
from TP_lib import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont,ImageOps
import os
import time

def writeToScreen(image):
    epd.displayPartial(epd.getbuffer(image))

def readPng(File, x, y, resize=False, basewidth=0, rotate=0):
    newimage = Image.open(os.path.join(picdir, File)).convert("RGBA")
    newimage     = newimage.rotate(rotate)
    if resize:
        wpercent = (basewidth/float(newimage.size[0]))
        hsize = int((float(newimage.size[1])*float(wpercent)))
        newimage = newimage.resize((basewidth,hsize), Image.ANTIALIAS)
    image.paste(newimage, (x, y), mask=newimage)

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')


picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PNG')

epd = epd2in13_V2.EPD_2IN13_V2()
gt = gt1151.GT1151()
GT_Dev = gt1151.GT_Development()
GT_Old = gt1151.GT_Development()

print("init and Clear")
epd.init(epd.FULL_UPDATE)
gt.GT_Init()
epd.Clear(0xFF)

image = Image.new("RGBA", (epd.width, epd.height), (255, 255, 255))
epd.displayPartBaseImage(epd.getbuffer(image))
DrawImage = ImageDraw.Draw(image)
epd.init(epd.PART_UPDATE)

#DrawImage.line((16, 60, 56, 60), fill = 0)
#epd.displayPartial(epd.getbuffer(image))
#time.sleep(5)
#DrawImage.line((16, 50, 56, 50), fill = 0)
#epd.displayPartial(epd.getbuffer(image))

#DrawImage.line((16, 60, 56, 60), fill = 0)
#DrawImage.line((16, 50, 56, 50), fill = 0)
#readPng("interface/arrow-down.png", 0, 10, True, 50)
#writeToScreen(image)
#readPng("interface/arrow-up.png", 0, 10, True, 50)

def draw_text_center(text, offsetx=2, offsety=2, size=24):
    font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), size)
    wi, hi = font.getsize (text)
    txt=Image.new('RGBA', (wi + offsetx, hi + offsety), (255,255,255))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), text, font = font, fill = 255)
    w=txt.rotate(90,  expand=1)
    image.paste(w, (int(epd.width/2 - hi/2), int(epd.height/2 - wi/2)))

def draw_text_at(text, x, y, offsetx=2, offsety=2, size=24):
    font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), size)
    wi, hi = font.getsize (text)
    txt=Image.new('RGBA', (wi + offsetx, hi + offsetx), (255,255,255))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), text, font = font, fill = 255)
    w=txt.rotate(90,  expand=1)
    image.paste(w, (x, y))

import datetime

while True:
    now = datetime.datetime.now()
    text = "{:02d}:{:02d}:{:02d}".format(now.hour, now.minute, now.second)
    draw_text_at(text, 0,0, offsety = 5, size=15)
    draw_text_center(text, offsety=5, size=50)
    writeToScreen(image)
    time.sleep(1)

# flash screen
#epd.init(epd.FULL_UPDATE)
#epd.displayPartBaseImage(epd.getbuffer(image))
#epd.init(epd.PART_UPDATE)

#epd.init(epd.PART_UPDATE)
#epd.Clear(255)
#DrawImage = ImageDraw.Draw(image)
#epd.init(epd.PART_UPDATE)
