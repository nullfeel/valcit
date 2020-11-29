import time, win32api, random, os
from threading import Thread
import serial
ard = serial.Serial('COM10', 9600) # Establish the connection on a specific port
# Record changes in shift
HIST = 0
x = 0
y = 0


GETKEY = win32api.GetKeyState
switch = 0

# List of hex key codes
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
def no_recoil():
    # 0x01: Left mouse button
    base_state = GETKEY(0x01)
    now, s = 0, ''

    while True:
        
        
        # Displayed text conf
        state_t = ['IDLE', 'SHOOTING'][now].center(10)
        switch_t = [' OFF', ' ON'][switch].center(10)
        print('\r                            ', state_t, switch_t, '', end='\r', sep='|')

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
            time.sleep(0.11)
            
            
            # Shifting vs reco
            if now:
                mouse_move()
                #mouse_move(x, y + shift_y) #Bermasalah
        except KeyboardInterrupt:
            print('\nNo Reco terminated!')
            no_recoil()

def mouse_move():  
    ard.write(b'1')
# Hotkeys
def switcher():
    global switch

    # 0xC0: ~ Key
    # 0x26: Up Arrow44
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
            
        time.sleep(0.11)
 
if __name__ == '__main__':
    print('''
                            |   STATE  |  SWITCH  
                             ---------- -----------''')

                             
    # Threading functions to allow live customization
    Thread(target=no_recoil).start()
    Thread(target=switcher).start()