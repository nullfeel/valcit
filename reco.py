import pyautogui as pg
import time, win32api, random, os
from threading import Thread
import serial
ard = serial.Serial('COM10', 9600) # Establish the connection on a specific port
# Record changes in shift
HIST = 0
def save_cfg():
    global HIST
    if shift_y != HIST:
        HIST = shift_y
        with open('v.cfg', 'w') as cfg:
            cfg.write(str(HIST))

# Getting saved value
shift_y = 0
if os.path.exists('v.cfg'):
    shift_y = int(open('v.cfg', 'r').read())

GETKEY = win32api.GetKeyState
switch = 0

# List of hex key codes
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
def no_recoil():
    # 0x01: Left mouse button
    base_state = GETKEY(0x01)
    now, s = 0, ''

    while True:
        
        # Record changes
        save_cfg()
        
        # Displayed text conf
        state_t = ['IDLE', 'SHOOTING'][now].center(10)
        switch_t = [' OFF', ' ON'][switch].center(10)
        s = shift_y
        if shift_y == 25:
            s = 'MAX - 25'
        if shift_y == 0:
            s = 'MIN - 0'
        shift_y_t = str(s).center(16)
        print('\r                            ', state_t, switch_t, shift_y_t, '', end='\r', sep='|')

        # If paused then skip
        if not switch:
            now = 0
            continue
        try:
            current_state = GETKEY(0x01)
            
            if current_state != base_state:
                base_state = current_state
                if current_state < 0:
                    now = 1
                else:
                    now = 0

            # Small delay to prevent eating thread
            time.sleep(0.001)
            
            
            # Shifting vs recoil
            if now:
                x, y = pg.position()
                mouse_move(x, y + shift_y) #Bermasalah
        except KeyboardInterrupt:
            print('\nNo Reco terminated!')
            no_recoil()

def mouse_move(x, y):
    bytes = x.to_bytes(4, byteorder = 'big') + y.to_bytes(4, byteorder = 'big') #Bermasalah
    ard.write(bytes)

# Hotkeys
def switcher():
    global switch, shift_y

    # 0xC0: ~ Key
    # 0x26: Up Arrow
    # 0x28: Down Arrow
    base_state = GETKEY(0xC0)
    base_up = GETKEY(0x26)
    base_down = GETKEY(0x28)
    
    while True:
        current_state = GETKEY(0xC0)
        current_up = GETKEY(0x26)
        current_down = GETKEY(0x28)
        
        # Pause/Resume script
        if current_state != base_state:
            base_state = current_state
            switch = 1 if current_state else 0                
            
        
        # Increase Reco shift
        if current_up != base_up:
            base_up = current_up
            if -1 < shift_y < 25:
                shift_y += 1
        
        # Decrease Reco shift
        if current_down != base_down:
            base_down = current_down
            if 0 < shift_y < 26:
                shift_y = abs(shift_y - 1)
            
        time.sleep(0.2)
 
if __name__ == '__main__':
    print('''
                            |   STATE  |  SWITCH  |  RECO SHIFT  |
                             ---------- ---------- ----------------''')
                             
    # Threading functions to allow live customization
    Thread(target=no_recoil).start()
    Thread(target=switcher).start()
