from SI4703Controller import SI4703Controller
import RPi.GPIO as GPIO
import time

while True:
  try:
    GPIO.setmode(GPIO.BCM)  
    resetPin     = 5
    intPin       = 6
    boardVersion = 2
    radio        = SI4703Controller(resetPin,intPin,boardVersion)
    radio.power_up()
    radio.config('USA')
    radio.force_mono()
    print ("tuning...")
    radio.tune(103.7)
    # ctrl.seek(1)
    while True:
      time.sleep(10)
  #    i = i + 0.2
  #    ctrl.tune(i) 
  #    print ("freq = {}".format(radio.read_freq()))
  #    print ("signal strength = {}".format(radio.get_signal_strength()))
  #    stereoType = "mono" if radio.get_stereo_indicator() == 0 else "stereo"
  #    print ("stereo type = {}".format(stereoType))
    
  except KeyboardInterrupt:
    break

  except IOError:
    GPIO.cleanup()
    radio._i2c.close()

GPIO.cleanup()
radio._i2c.close()

