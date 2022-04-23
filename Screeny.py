#!/usr/bin/python
# -*- coding:utf-8 -*-

from TP_lib import gt1151
from TP_lib import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont,ImageOps
import os
import time
import threading
import requests
from io import BytesIO
import datetime
from functools import partial

flag_t = 1

epd = epd2in13_V2.EPD_2IN13_V2()
gt = gt1151.GT1151()
GT_Dev = gt1151.GT_Development()
GT_Old = gt1151.GT_Development()

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PNG')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')


def writeToScreen(image):
    epd.displayPartial(epd.getbuffer(image))

def pthread_irq() :
    print("pthread running")
    while flag_t == 1 :
        if(gt.digital_read(gt.INT) == 0) :
            GT_Dev.Touch = 1
        else :
            GT_Dev.Touch = 0
        gt.GT_Scan(GT_Dev, GT_Old)
    print("thread:exit")

def pthreadscreen():
    while True:
        gt.GT_Scan(GT_Dev, GT_Old)
        time.sleep(0.1)

def getJSONfromURL(url):
    resp = requests.get(url=url)
    return resp.json()

t = threading.Thread(target = pthread_irq)
t.setDaemon(True)
t.start()

ViewManager = {
    "currentView": None,
    "views": {},
    "clear": False
}

def ChangeViewTo(v):
    ViewManager['currentView'] = ViewManager["views"][v]
    ViewManager['currentView'].prehook()

def ClearView():
    ViewManager["clear"] = True

class View():
    def __init__(self, epd, gt, mainLayer):
        self.epd = epd
        self.gt = gt
        self.mainLayer = mainLayer
        self.buffer = ImageDraw.Draw(mainLayer)
        self.actions = {}

    def draw(self):
        pass

    def prehook(self):
        pass

    def writeToScreen(self):
        self.epd.init(epd.PART_UPDATE)
        self.epd.displayPartial(self.epd.getbuffer(self.mainLayer))

    def addLayer(self, layer, x, y, mask=None):
        self.mainLayer.paste(layer, (x,y), mask)

    def readPngFromFile(self, layer, path, x, y, resize=False, basewidth=0, rotate=0):
        img = Image.open(path).convert("RGBA")
        return self.readPng(layer, img, x, y, resize, basewidth, rotate)

    def readPngFromURL(self, layer, url, x, y, resize=False, basewidth=0, rotate=0):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        self.readPng(layer, img, x, y, resize, basewidth, rotate)

    def readPng(self, layer, img, x, y, resize=False, basewidth=0, rotate=0):
        img = img.rotate(rotate)
        if resize:
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        layer.paste(img, (x, y), mask=img)
        return img

    def registerAction(self, name, x1, y1, x2, y2, cb):
        self.actions[name] = [x1, y1, x2, y2, cb]
        #if GT_Dev.Touch == 1 and x1 <= GT_Dev.X[0] and GT_Dev.X[0] >= x2 and y1 <= GT_Dev.Y[0] and GT_Dev.Y[0] >= y2:
            #cb()

    def draw_text_center(self, layer, text, offsetx=2, offsety=2, size=24):
        width = layer.size[0]
        height = layer.size[1]
        font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), size)
        wi, hi = font.getsize (text)
        txt=Image.new('RGBA', (wi + offsetx, hi + offsety), (255,255,255))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), text, font = font, fill = 255)
        w=txt.rotate(90,  expand=1)
        layer.paste(w, (int(width/2 - hi/2), int(height/2 - wi/2)))

    def draw_text_at(self, layer, text, x, y, offsetx=2, offsety=2, size=24):
        font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), size)
        wi, hi = font.getsize (text)
        txt=Image.new('RGBA', (wi + offsetx, hi + offsetx), (255,255,255))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), text, font = font, fill = 255)
        w=txt.rotate(90,  expand=1)
        layer.paste(w, (x, y))

    def draw_rect(self, drawcontext, xy, outline=None, width=0):
        (x1, y1, x2, y2) = xy
        points = (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
        drawcontext.line(points, fill=outline, width=width)

    def runActions(self):
        for actionKey in self.actions:
            action = self.actions[actionKey]
            if action[0] <= GT_Dev.X[0] <= action[2] and action[1] <= GT_Dev.Y[0] <= action[3]:
                print("-------------")
                print("Run action : " + actionKey)
                print(( GT_Dev.X[0],  GT_Dev.Y[0]))
                print(action)
                action[4]()
                break

class BottomMenuView(View):
    def __init__(self, epd, gt, mainLayer):
        super().__init__(epd, gt, mainLayer)
        self.menuLayer = Image.new("RGBA", (25, epd.height), (255, 255, 255))
        self.menuBuffer = ImageDraw.Draw(self.menuLayer)

    def drawHomeButton(self, layer):
        offset = 26
        img =  self.readPngFromFile(layer, os.path.join(picdir, "interface/home.png"), 0, self.epd.height - offset, True, 25, 90)
        self.registerAction("home", self.epd.width - 25, self.epd.height - offset, self.epd.width - 25 + img.size[0], self.epd.height - offset + img.size[1], partial(ChangeViewTo, "hub"))

    def drawHome2Button(self, layer):
        offset = 100
        img = self.readPngFromFile(layer, os.path.join(picdir, "interface/home.png"), 0, self.epd.height - offset, True, 25, 90)
        self.registerAction("home2", self.epd.width - 25, self.epd.height - offset, self.epd.width - 25 + img.size[0], self.epd.height - offset + img.size[1], partial(ChangeViewTo, "home"))

    def drawSyncButton(self, layer):
        offset = self.epd.height
        img = self.readPngFromFile(layer, os.path.join(picdir, "interface/sync.png"), 0, self.epd.height - offset, True, 25, 90)
        self.registerAction("refresh", self.epd.width - 25, self.epd.height - offset, self.epd.width - 25 + img.size[0], self.epd.height - offset + img.size[1], ClearView)


    def draw(self):
        self.menuBuffer.line((0, 0, 0, self.epd.height), fill = 0)
        self.drawHomeButton(self.menuLayer)
        self.drawHome2Button(self.menuLayer)
        self.drawSyncButton(self.menuLayer)
        self.addLayer(self.menuLayer, self.epd.width - 25, 0)
        return super().draw()

class HomeView(View):
    def __init__(self, epd, gt, mainLayer):
        super().__init__(epd, gt, mainLayer)
        self.homeLayer = Image.new("RGBA", (epd.width - 25, epd.height), (255, 255, 255))
        self.homeBuffer = ImageDraw.Draw(self.homeLayer)

    def draw(self):
        self.draw_text_center(self.homeLayer, "Home")
        self.addLayer(self.homeLayer, 0, 0)
        return super().draw()

class ComponentView(View):
    def __init__(self, epd, gt, mainLayer):
        super().__init__(epd, gt, mainLayer)
        self.viewLayer = Image.new("RGBA", (epd.width - 25, epd.height), (255, 255, 255))
        self.viewBuffer = ImageDraw.Draw(self.viewLayer)

class CryptoView(ComponentView):
    def __init__(self, epd, gt, mainLayer):
        super().__init__(epd, gt, mainLayer)
        self.coins = ["bitcoin", "ethereum", "moonbeam"]
        self.index = 0
        self.canDraw = True
        self.increaseTime = 0

    def prehook(self):
        self.canDraw = True

    def increaseCount(self):
        if not self.increaseTime < datetime.datetime.now().timestamp():
            return
        self.increaseTime = datetime.datetime.now().timestamp() + 1
        self.index = (self.index + 1) % len(self.coins) 
        self.canDraw = True

    def draw(self):
        if not self.canDraw:
            return
        self.viewBuffer.rectangle((0, 0, self.viewLayer.size[0], self.viewLayer.size[1]), fill = (255, 255, 255))
        self.draw_text_center(self.viewLayer, "Loading...", size=50)
        self.addLayer(self.viewLayer, 0, 0)
        self.writeToScreen()
        self.viewBuffer.rectangle((0, 0, self.viewLayer.size[0], self.viewLayer.size[1]), fill = (255, 255, 255))
        self.canDraw = False
        data = getJSONfromURL("https://api.coingecko.com/api/v3/coins/" + self.coins[self.index] + "?localization=false")
        name = data["name"]
        imgURL = data["image"]["large"]
        price = data["market_data"]["current_price"]["usd"]
        self.viewBuffer.rectangle((0, 0, self.viewLayer.size[0], self.viewLayer.size[1]), fill = (255, 255, 255))
        self.readPngFromURL(self.viewLayer, imgURL, 5, epd.height - 100, True, 90, rotate=90)
        self.draw_text_at(self.viewLayer, name, 10, 50, size=20)
        self.draw_text_at(self.viewLayer, str(price) + "$", 50, 5, size=40)
        self.registerAction("next", 0, 0, self.viewLayer.size[0], self.viewLayer.size[1], partial(self.increaseCount))
        self.addLayer(self.viewLayer, 0, 0)

class ClockView(ComponentView):
    def draw(self):
        now = datetime.datetime.now()
        text = "{:02d}:{:02d}:{:02d}".format(now.hour, now.minute, now.second)
        self.draw_text_center(self.viewLayer, text, offsety=5, size=50)
        self.addLayer(self.viewLayer, 0, 0)

class HUBView(View):
    def __init__(self, epd, gt, mainLayer):
        super().__init__(epd, gt, mainLayer)
        self.hub = [{"name": "Clock", "icon": "interface/clock.png", "view": "clock"},{"name": "Crypto", "icon": "currency/dollar.png", "view": "crypto"} ]
        self.index = 0
        self.viewLayer = Image.new("RGBA", (epd.width - 25, epd.height), (255, 255, 255))
        self.viewBuffer = ImageDraw.Draw(self.viewLayer)

    def drawBlock(self, i):
        x = 15
        y = int(self.viewLayer.size[1] - 40) - i * 40
        if i > 0:
            y = y - 15
        name = self.hub[i]["name"]
        font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 15)
        wi, hi = font.getsize(name)
        img = self.readPngFromFile(self.viewLayer, os.path.join(picdir, self.hub[i]["icon"]), x, y, True, 35, 90)
        self.draw_rect(self.viewBuffer, (x, y, x+img.size[0], y+img.size[1]), outline = 0, width=2)
        self.draw_text_at(self.viewLayer, name,x + img.size[0] + 1, y - int(img.size[1]/2) + int(hi/2) - 1, size=15)
        self.registerAction(name, x, y, x+img.size[0], y+img.size[1], partial(ChangeViewTo, self.hub[i]["view"]))


    def draw(self):
        for i in range(0, len(self.hub)):
            self.drawBlock(i)
        self.addLayer(self.viewLayer, 0, 0)
        return super().draw()

class Home2View(View):
    def __init__(self, epd, gt, mainLayer):
        super().__init__(epd, gt, mainLayer)
        self.homeLayer = Image.new("RGBA", (epd.width - 25, epd.height), (255, 255, 255))
        self.homeBuffer = ImageDraw.Draw(self.homeLayer)

    def draw(self):
        self.draw_text_center(self.homeLayer, "Home2")
        self.addLayer(self.homeLayer, 0, 0)
        return super().draw()


epd.init(epd.FULL_UPDATE)
gt.GT_Init()
epd.Clear(0xFF)

image = Image.new("RGBA", (epd.width, epd.height), (255, 255, 255))
epd.displayPartBaseImage(epd.getbuffer(image))
epd.init(epd.PART_UPDATE)

B = BottomMenuView(epd, gt, image)
B.draw()
B.writeToScreen()
print(B.actions)
ViewManager["views"]["home"] = HomeView(epd, gt, image)
ViewManager["views"]["home2"] = Home2View(epd, gt, image)
ViewManager["views"]["hub"] = HUBView(epd, gt, image)
ViewManager["views"]["clock"] = ClockView(epd, gt, image)
ViewManager["views"]["crypto"] = CryptoView(epd, gt, image)
ViewManager["currentView"] = ViewManager["views"]["hub"]

refreshTime = 0
while True:
    if ViewManager["clear"] or refreshTime < datetime.datetime.now().timestamp():
        refreshTime = datetime.datetime.now().timestamp() + 120
        ViewManager["clear"] = False
        epd.init(epd.FULL_UPDATE)
        epd.displayPartBaseImage(epd.getbuffer(image))
        epd.init(epd.PART_UPDATE)
        B.draw()

    ViewManager["currentView"].draw()
    ViewManager["currentView"].writeToScreen()

    if(GT_Dev.TouchpointFlag):
        GT_Dev.TouchpointFlag = 0
        ViewManager["currentView"].runActions()
        B.runActions()
    time.sleep(0.00001)

