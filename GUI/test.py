import time
import os
import RPi.GPIO as GPIO
import sys
sys.path.append("..")

from ColorConstants                  import *
from Si4703.SI4703Constants          import SI4703_POWER_CONFIG_SEEKUP_UP, SI4703_POWER_CONFIG_SEEKUP_DOWN
from GUIPageManager                  import GUIPageManager
from Si4703.SI4703Controller         import SI4703Controller

debug = True

if not debug:
  os.putenv('SDL_VIDEODRIVER', 'fbcon')
  os.putenv('SDL_FBDEV', '/dev/fb1')
  os.putenv('SDL_MOUSEDRV', 'TSLIB')
  os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

resetPin     = 5
intPin       = 6
boardVersion = 2
GPIO.setmode(GPIO.BCM)
radio = SI4703Controller(resetPin,intPin,boardVersion)
radio.power_up()
radio.config('USA')

######################################################################################################
#                                             Transitions                                            #          
######################################################################################################

# page0 -> page1
def p0_button0_callback():
  manager.turn_to_page(page1)

# page0 -> page2
def p0_button1_callback():
  manager.turn_to_page(page2)

manager    = GUIPageManager(debug = debug)

######################################################################################################
#                                        Main page: page0                                            #
#                                                                                                    #
# button0: turn to transmitter page                                                                  #
# button1: turn to receiver page                                                                     #            
######################################################################################################

page0         = manager.add_page()
p0_button0    = page0.add_button("Transmitter", (160, 80), 40, WHITE, call_back = p0_button0_callback)
p0_button1    = page0.add_button("Receiver", (160, 140), 40, WHITE, call_back = p0_button1_callback)

######################################################################################################
#                                     Transmitter page: page1                                        #          
######################################################################################################

page1         = manager.add_page()
page1.add_back_button()

######################################################################################################
#                                      Receiver page: page2                                          #          
######################################################################################################

def p2_button0_callback():
  time.sleep(0.5)
  radio.user_seek(SI4703_POWER_CONFIG_SEEKUP_UP)

page2         = manager.add_page()
p2_button0    = page2.add_button("seek", (160, 80), 40, WHITE, call_back = p2_button0_callback)
page2.add_back_button()

# turn on the manager
manager.control_enable()

while manager.on:
  try:
    #time.sleep(1)
    manager.render()
  except KeyboardInterrupt:
    break
  except IOError:
    pass

GPIO.cleanup()
radio._i2c.close()
print "script exited"

