import keyboard
import serial
import time
import ctypes
import PIL.ImageGrab
import PIL.Image
import random 
import os
import mss
from threading import Thread

from colorama import Fore, Style, init
S_HEIGHT, S_WIDTH = (PIL.ImageGrab.grab().size)
PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
TOLERANCE = 60
GRABZONE = 10
TRIGGER_KEY = "ctrl + alt"
SWITCH_KEY = "ctrl + tab"
GRABZONE_KEY_UP = "ctrl + up"
GRABZONE_KEY_DOWN = "ctrl + down"
mods = ["slow", "medium", "fast"]


ard = serial.Serial('COM10', 9600) # Establish the connection on a specific port
#Credit to SixFourSeven-2077

class FoundEnemy(Exception):
    pass

class dotBot():
    def __init__(self):
        self.toggled = False
        self.mode = 1
        self.last_reac = 0

    def toggle(self):
        self.toggled = not self.toggled

    def switch(self):
        if self.mode != 2:
            self.mode += 1
    def click(self):
        ard.write(b'1') # Send Bytes Data to Arduitod
    
    def approx(self, r, g ,b):
        return PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE and PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE and PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE

    def grab(self):
        with mss.mss() as sct:
            bbox=(int(S_HEIGHT/2-GRABZONE), int(S_WIDTH/2-GRABZONE), int(S_HEIGHT/2+GRABZONE), int(S_WIDTH/2+GRABZONE))
            #monitor = {"top": S_HEIGHT/2-GRABZONE, "left": S_WIDTH/2-GRABZONE, "width": GRABZONE*2, "height": GRABZONE*2}
            sct_img = sct.grab(bbox)
            # Convert to PIL/Pillow Image
            return PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    def scan(self):
        start_time = time.time()
        # == 50~ms
        # pmap = PIL.ImageGrab.grab(bbox=(S_HEIGHT/2-GRABZONE, S_WIDTH/2-GRABZONE, S_HEIGHT/2+GRABZONE, S_WIDTH/2+GRABZONE))
        pmap = self.grab()
        
        try:
            for x in range(0, GRABZONE*2):
                for y in range(0, GRABZONE*2):
                    r, g, b = pmap.getpixel((x,y))
                    if self.approx(r, g, b):
                        raise FoundEnemy
        except FoundEnemy:
            self.last_reac = int((time.time() - start_time)*1000)
            self.click()
            if self.mode == 0:
                time.sleep(0.5)
            if self.mode == 1:
                time.sleep(0.25)
            if self.mode == 2:
                time.sleep(0.12)
            print_banner(self)

def print_banner(bot: dotBot):
    os.system("cls")
    print (Style.BRIGHT + Fore.GREEN + """
#### ##    ##  #######   ######  #### ######## 
 ##  ###   ## ##     ## ##    ##  ##     ##    
 ##  ####  ## ##     ## ##        ##     ##    
 ##  ## ## ## ##     ## ##        ##     ##    
 ##  ##  #### ##     ## ##        ##     ##    
 ##  ##   ### ##     ## ##    ##  ##     ##    
#### ##    ##  #######   ######  ####    ##       
                INOCIT FrostFex beta 0.2""" + Style.RESET_ALL)
    print(" Status Trigger:",  (Fore.GREEN if bot.toggled else Fore.RED) + str(bot.toggled) + Style.RESET_ALL )
    print(" Mode :", mods[bot.mode])
    print(" Fov:", str(GRABZONE) + "x" + str(GRABZONE))
    print(" React time:", str(bot.last_reac) + " ms ("+str((bot.last_reac)/(GRABZONE*GRABZONE))+"ms/pix)")
    


if __name__ == "__main__":
    bot = dotBot()
    print_banner(bot)
    while True:
        if keyboard.is_pressed(SWITCH_KEY):
            bot.switch()
            print_banner(bot)
            while keyboard.is_pressed(SWITCH_KEY):
                pass
        if keyboard.is_pressed(GRABZONE_KEY_UP):
            GRABZONE += 5
            print_banner(bot)
            while keyboard.is_pressed(GRABZONE_KEY_UP):
                pass
        if keyboard.is_pressed(GRABZONE_KEY_DOWN):
            GRABZONE -= 5
            print_banner(bot)
            while keyboard.is_pressed(GRABZONE_KEY_DOWN):
                pass
        if keyboard.is_pressed(TRIGGER_KEY):
            bot.toggle()
            print_banner(bot)
            while keyboard.is_pressed(TRIGGER_KEY):
                pass
        if bot.toggled:
            bot.scan()