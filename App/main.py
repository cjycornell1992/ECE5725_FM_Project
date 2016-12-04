import time
import os
import RPi.GPIO as GPIO
import sys
import glob

sys.path.append("..")

from GUI.ColorConstants              import *
from Si4703.SI4703Constants          import SI4703_POWER_CONFIG_SEEKUP_UP, SI4703_POWER_CONFIG_SEEKUP_DOWN
from Si4703.SI4703Constants          import SI4703_POWER_CONFIG_DMUTE_EN, SI4703_POWER_CONFIG_DMUTE_DIS
from GUI.GUIPageManager              import GUIPageManager
from Si4703.SI4703Controller         import SI4703Controller
from Transmitter.Transmitter         import Transmitter
from Transmitter.WaveReaderException import WaveReaderException

######################################################################################################
#                                          Environment Setup                                         #          
######################################################################################################
debug = True

if not debug:
  os.putenv('SDL_VIDEODRIVER', 'fbcon')
  os.putenv('SDL_FBDEV', '/dev/fb1')
  os.putenv('SDL_MOUSEDRV', 'TSLIB')
  os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

######################################################################################################
#                                           Receiver Setup                                           #          
######################################################################################################
resetPin     = 5
intPin       = 6
boardVersion = 2
GPIO.setmode(GPIO.BCM)
radio = SI4703Controller(resetPin,intPin,boardVersion)
radio.power_up()
radio.config('USA')

######################################################################################################
#                                          Transmitter Setup                                         #          
######################################################################################################

""" playList : a list of strings, relative path. 
    Example: a = glob.glob('../Transmitter/wav/*.wav')
             a will be ['../Transmitter/wav/bird.wav', '../Transmitter/wav/star_wars.wav']
"""
playList    = glob.glob('../Transmitter/wav/*.wav')
transmitter = Transmitter(100.1, playList[0])
transmitter.init()

######################################################################################################
#                                             Transitions                                            #          
######################################################################################################

# page0 -> page1
def p0_button0_callback():
  manager.turn_to_page(page1)

# page0 -> page2
def p0_button1_callback():
  manager.turn_to_page(page2)

# page3 -> page2 (after pressing "go" in the keypad)
# p3_button12_callback

manager    = GUIPageManager(debug = debug)

######################################################################################################
#                                        Main page: page0                                            #
#                                                                                                    #
# button0: turn to transmitter page                                                                  #
# button1: turn to receiver page                                                                     #            
######################################################################################################

page0         = manager.add_page()
p0_button0    = page0.add_button("Transmitter", (160, 80), 40, CYAN, call_back = p0_button0_callback)
p0_button1    = page0.add_button("Receiver", (160, 140), 40, CYAN, call_back = p0_button1_callback)

######################################################################################################
#                                     Transmitter page: page1                                        #          
######################################################################################################
tune_fre = ""
transmitter_fre = 0
def p1_button0_callback():
  manager.turn_to_page(page3)


page1         = manager.add_page()
p1_button0    = page1.add_button("Tune", (60, 200), 60, PURPLE, call_back = p1_button0_callback)
page1.add_back_button()


######################################################################################################
#                                      Receiver page: page2                                          #
#                                                                                                    #
# button0: seekup                                                                                    # 
# button1: seekdown                                                                                  #
# button2: volume up                                                                                 #
# button3: volume down                                                                               #
# button4: turn to page3                                                                             #
# p2_fre:  frequency information                                                                     #
# p2_vol:  volume information                                                                        #          
######################################################################################################

receiver_fre = 0
vol = 50
mute_flag = SI4703_POWER_CONFIG_DMUTE_DIS
page2          = manager.add_page()
# FM frequency information
p2_fre         = page2.add_button("---.-", (160, 40), 60, SKY_BLUE)
# volume information
p2_vol         = page2.add_button("Vol:" + str(vol), (160, 120), 50, YELLOW_GREEN)

def p2_button0_callback():
  time.sleep(0.5)
  radio.mute(SI4703_POWER_CONFIG_DMUTE_DIS)
  radio.user_seek(SI4703_POWER_CONFIG_SEEKUP_UP)
  global receiver_fre, p2_fre
  receiver_fre = radio.get_freq()
  p2_fre.update_text(str(receiver_fre) + "MHz")

def p2_button1_callback():
  time.sleep(0.5)
  radio.mute(SI4703_POWER_CONFIG_DMUTE_DIS)
  radio.user_seek(SI4703_POWER_CONFIG_SEEKUP_DOWN)
  global receiver_fre, p2_fre
  receiver_fre = radio.get_freq()
  p2_fre.update_text(str(receiver_fre) + "MHz")

def p2_button2_callback():
  global vol, p2_vol
  vol = min(100, vol + 10)
  radio.set_volume(vol)
  p2_vol.update_text("Vol:" + str(vol))

def p2_button3_callback():
  global vol, p2_vol
  vol = max(0, vol - 10)
  radio.set_volume(vol)
  p2_vol.update_text("Vol:" + str(vol))

def p2_button4_callback():
  manager.turn_to_page(page3)

def p2_button5_callback():
  global mute_flag
  mute_flag = (mute_flag + 1) % 2
  print mute_flag
  radio.mute(mute_flag)

def p2_back_extra():
  radio.mute(SI4703_POWER_CONFIG_DMUTE_EN)  
  global p2_fre
  p2_fre.update_text("---.-")

p2_button0     = page2.add_button(">>|", (240, 80), 40, SKY_BLUE, call_back = p2_button0_callback)
p2_button1     = page2.add_button("|<<", (80, 80), 40, SKY_BLUE, call_back = p2_button1_callback)
p2_button2     = page2.add_button("+", (240, 120), 80, YELLOW_GREEN, call_back = p2_button2_callback)
p2_button3     = page2.add_button("-", (80, 120), 80, YELLOW_GREEN, call_back = p2_button3_callback)
p2_button4     = page2.add_button("Tune", (60, 200), 60, PURPLE, call_back = p2_button4_callback)
p2_button5     = page2.add_button(">||", (160, 80), 40, SKY_BLUE, call_back = p2_button5_callback)

p2_back_button = page2.add_back_button()
p2_back_button.extra_callback(p2_back_extra) 

######################################################################################################
#                                      Receiver page: page3, user specify the frequency              #
# button0~9 number 0~9                                                                               #
# button10 dot                                                                                       #
# button11 backspace(delete one digit)                                                               #
# button12 Go, tune to the fre                                                                       #           
######################################################################################################
page3          = manager.add_page()
p3_fre         = page3.add_button("---.-", (160, 40), 60, WHITE)

def update_tune_fre(num):
  global tune_fre
  print tune_fre
  if len(tune_fre) <= 4:
    tune_fre += num
    p3_fre.update_text(tune_fre)
	
def p3_button1_callback():
  update_tune_fre("1")

def p3_button2_callback():
  update_tune_fre("2")

def p3_button3_callback():
  update_tune_fre("3")

def p3_button4_callback():
  update_tune_fre("4")

def p3_button5_callback():
  update_tune_fre("5")

def p3_button6_callback():
  update_tune_fre("6")

def p3_button7_callback():
  update_tune_fre("7")

def p3_button8_callback():
  update_tune_fre("8")

def p3_button9_callback():
  update_tune_fre("9")

def p3_button10_callback():
  global tune_fre
  if not "." in tune_fre:
    update_tune_fre(".")

def p3_button0_callback():
  update_tune_fre("0")

def p3_button11_callback():
  global tune_fre
  if len(tune_fre) > 0:
    tune_fre = tune_fre[0:len(tune_fre) - 1]
  p3_fre.update_text(tune_fre)


def p3_button12_callback():
  global receiver_fre, tune_fre, p2_fre, p3_fre, transmitter_fre
  try:
    fre = float(tune_fre)
    fre = min(fre, 107.9)
    fre = max(fre, 87.5)
    if page3.parentNum == 1:
	# set the transmitter frequency
      transmitter_fre = fre
      manager.turn_to_page(page1, set_parent = False)
    elif page3.parentNum == 2:
      # set the receiver frequency
      receiver_fre = fre
      radio.mute(SI4703_POWER_CONFIG_DMUTE_DIS)
      radio.tune(receiver_fre)
      p2_fre.update_text(str(receiver_fre) + "MHz")
      manager.turn_to_page(page2, set_parent = False)
  except ValueError:
    p3_fre.update_text("Invalid value")
    time.sleep(1)
  p3_fre.update_text("---.-")
  tune_fre = ""

p3_button1     = page3.add_button("1", (80, 80), 50, WHITE, call_back = p3_button1_callback)
p3_button2     = page3.add_button("2", (120, 80), 50, WHITE, call_back = p3_button2_callback)
p3_button3     = page3.add_button("3", (160, 80), 50, WHITE, call_back = p3_button3_callback)
p3_button4     = page3.add_button("4", (80, 120), 50, WHITE, call_back = p3_button4_callback)
p3_button5     = page3.add_button("5", (120, 120), 50, WHITE, call_back = p3_button5_callback)
p3_button6     = page3.add_button("6", (160, 120), 50, WHITE, call_back = p3_button6_callback)
p3_button7     = page3.add_button("7", (80, 160), 50, WHITE, call_back = p3_button7_callback)
p3_button8     = page3.add_button("8", (120, 160), 50, WHITE, call_back = p3_button8_callback)
p3_button9     = page3.add_button("9", (160, 160), 50, WHITE, call_back = p3_button9_callback)
p3_button10    = page3.add_button(".", (80, 200), 50, WHITE, call_back = p3_button10_callback)
p3_button0     = page3.add_button("0", (120, 200), 50, WHITE, call_back = p3_button0_callback)
p3_button11    = page3.add_button("<-", (160, 200), 50, WHITE, call_back = p3_button11_callback)
p3_button12    = page3.add_button("Go", (280, 100), 50, WHITE, call_back = p3_button12_callback)

# back button
p3_back_button = page3.add_back_button()

# turn on the manager
manager.control_enable()

while manager.on:
  try:
    #time.sleep(1)
    manager.render()
  except KeyboardInterrupt:
    manager.control_disable()
  except IOError:
    pass
  except WaveReaderException, error:
    print "error: {}".format(error)

GPIO.cleanup() 
radio._i2c.close()
transmitter.close()
print "script exited"

