from SI4703Controller import SI4703Controller
from SI4703Constants  import SI4703_POWER_CONFIG_SEEKUP_DOWN
from SI4703Constants  import SI4703_POWER_CONFIG_SEEKUP_UP
import RPi.GPIO as GPIO
import time

def seekup_callback(channel):
  # receivable channels at ithaca:
  # [ FM 88.1 88.9 91.7 93.5 97.3 103.7 107.1 MHz]
  #radio.tune(107.1) 
  radio.user_seek(SI4703_POWER_CONFIG_SEEKUP_UP)
  time.sleep(0.1)
  print ("freq = {}".format(radio.get_freq()))
  print ("signal strength = {}".format(radio.get_signal_strength()))

def seekdown_callback(channel):
  # receivable channels at ithaca:
  # [ FM 88.1 88.9 91.7 93.5 97.3 103.7 107.1 MHz]
  #radio.tune(107.1) 
  radio.user_seek(SI4703_POWER_CONFIG_SEEKUP_DOWN)
  time.sleep(0.1)
  print ("freq = {}".format(radio.get_freq()))
  print ("signal strength = {}".format(radio.get_signal_strength()))

while True:
  try:
    seekUpPin    = 27
    seekDownPin  = 23
    resetPin     = 5
    intPin       = 6
    boardVersion = 2
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup([seekUpPin, seekDownPin], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(seekUpPin, GPIO.FALLING, callback=seekup_callback, bouncetime = 500)
    GPIO.add_event_detect(seekDownPin, GPIO.FALLING, callback=seekdown_callback, bouncetime = 500)
    radio = SI4703Controller(resetPin,intPin,boardVersion)
    radio.power_up()
    radio.config('USA')
    
    while True:
      time.sleep(10)
  
  except KeyboardInterrupt:
    break

  except IOError:
    GPIO.cleanup()
    radio._i2c.close()

GPIO.cleanup()
radio._i2c.close()

