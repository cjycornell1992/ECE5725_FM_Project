from SI4703Constants import *
import RPi.GPIO as GPIO
import smbus
import time
import sys

class SI4703Controller:
  """drivers for SI4703"""
  def __init__(self, resetPin, intPin, piVersion):
    self._resetPin      = resetPin
    self._intPin        = intPin
    self._i2c           = smbus.SMBus(1 if (piVersion == 2) else 0)
    self._i2cAddr       = SI4703_I2C_ADDR
    self._readReg       = []
    self._reset()

  def _id_check(self):
    deviceIDWordData      = self.read_one_reg(SI4703_DEVICE_ID_ADDR)
    chipIDWordData        = self.read_one_reg(SI4703_CHIP_ID_ADDR)
                                               # word            mask                          lsb
    partNumber            = self._extract_bits(deviceIDWordData, SI4703_DEVICE_ID_PN_MASK,     SI4703_DEVICE_ID_PN_LSB     ) 
    manufactureID         = self._extract_bits(deviceIDWordData, SI4703_DEVICE_ID_MFGID_MASK,  SI4703_DEVICE_ID_MFGID_LSB  ) 
    chipRevision          = self._extract_bits(chipIDWordData,   SI4703_CHIP_ID_REV_MASK,      SI4703_CHIP_ID_REV_LSB      ) 
    chipDeviceID          = self._extract_bits(chipIDWordData,   SI4703_CHIP_ID_DEV_MASK,      SI4703_CHIP_ID_DEV_LSB      ) 
    chipFirmware          = self._extract_bits(chipIDWordData,   SI4703_CHIP_ID_FIRMWARE_MASK, SI4703_CHIP_ID_FIRMWARE_LSB )         
    if (partNumber != SI4703_DEVICE_ID):
      sys.stderr.write('DEVICE ID unmatch, read out value: {}\n'.format(partNumber))
      sys.exit(-1)
    if (manufactureID != SI4703_MANUFACTURE_ID):
      sys.stderr.write('Manufacture ID unmatch, read out value: {}\n'.format(manufactureID))
      sys.exit(-1)
    if (chipRevision != SI4703_CHIP_ID_REV_C):
      sys.stderr.write('Manufacture ID unmatch, read out value: {}\n'.format(chipRevision))
      sys.exit(-1)
    if (chipDeviceID != SI4703_CHIP_ID_DEV_BEFORE_UP):
      sys.stderr.write('chip DEV ID unmatch, read out value: {}\n'.format(chipDeviceID))
      sys.exit(-1)
    if (chipFirmware != SI4703_CHIP_ID_FIRMWARE_BEFORE_UP):
      sys.stderr.write('chip Firmware ID unmatch, read out value: {}\n'.format(chipFirmware))
      sys.exit(-1)
    print ("device family: Si4702/03")
    print ("Manufacture ID: 0x242")
    print ("Chip Version: Revision C")
    print ("Chip Device: Si4703")


  def _reset(self):
    GPIO.setup(self._resetPin, GPIO.OUT)
    GPIO.output(self._resetPin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(self._resetPin, GPIO.HIGH)

  def _extract_bits(self, word, mask, lsb):
    return (word & mask) >> lsb

  def read_one_reg(self, reg_addr):
    self._readReg = self._i2c.read_i2c_block_data(self._i2cAddr, 0, SI4703_REG_NUM * 2) # bring all registers, each register has two bytes
    upperByteIdx  = 2 * (SI4703_REG_NUM + reg_addr - SI4703_RD_ADDR_START) % SI4703_REG_NUM
    lowerByteIdx  = upperByteIdx + 1
    upperByte     = self._readReg[upperByteIdx]
    lowerByte     = self._readReg[lowerByteIdx]
    wordData      = (upperByte << 8) | lowerByte
    return wordData

  def power_up(self):
    self._id_check()

try:
  GPIO.setmode(GPIO.BCM)
  ctrl = SI4703Controller(5,13,2)
  # print format((ctrl.read_one_reg(SI4703_I2C_ADDR)),'04x')
  ctrl.power_up()

except:
  pass

GPIO.cleanup()