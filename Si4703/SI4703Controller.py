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
    self._wr_rd_offest  = ((SI4703_RD_ADDR_START - SI4703_WR_ADDR_START) << 1) + 1
    self._readReg       = []
    self._reset()

  def _id_check(self):
    # sync buffer & i2c device first, then read one reg
    self._sync_read_reg()
    deviceIDWordData      = self._read_one_reg(SI4703_DEVICE_ID_ADDR)
    chipIDWordData        = self._read_one_reg(SI4703_CHIP_ID_ADDR)
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
    # 1 ms
    time.sleep(0.001)
    GPIO.output(self._resetPin, GPIO.HIGH)

  def _extract_bits(self, word, mask, lsb):
    return (word & mask) >> lsb	  

  def _set_bits(self, old_word, value, mask, lsb):
    toggledMask = mask ^ 0xffff
    return (value << lsb) | (old_word & toggledMask)

  def _sync_read_reg(self):
    self._readReg = self._i2c.read_i2c_block_data(self._i2cAddr, 0, SI4703_REG_NUM << 1) # bring all registers, each register has two bytes
    
  def _read_one_reg(self, reg_addr):
    # read from the buffer, needs to be read synced first
    upperByteIdx  = ((SI4703_REG_NUM + reg_addr - SI4703_RD_ADDR_START) % SI4703_REG_NUM) << 1 # index in the buffer
    lowerByteIdx  = upperByteIdx + 1
    upperByte     = self._readReg[upperByteIdx]
    lowerByte     = self._readReg[lowerByteIdx]
    wordData      = (upperByte << 8) | lowerByte
    return wordData

  def _write_one_reg(self, reg_addr, word):
    # write to the buffer, needs to be followed with a write sync
    upperByteIdx  = ((SI4703_REG_NUM + reg_addr - SI4703_RD_ADDR_START) % SI4703_REG_NUM) << 1 # index in the buffer
    lowerByteIdx  = upperByteIdx + 1
    self._readReg[upperByteIdx] = word >> 8
    self._readReg[lowerByteIdx] = word & 0x00ff

  def _rotate_read_reg(self): 
    return self._readReg[self._wr_rd_offest:] + self._readReg[:self._wr_rd_offest]
    
  def _write_sync(self):
    write_buffer = self._rotate_read_reg()
    self._i2c.write_i2c_block_data(self._i2cAddr, 0, write_buffer)
  
  def _enable_oscillator(self):
    # set XOSCEN bit in Test 1 register
    readWord  = self._read_one_reg(SI4703_TEST1_ADDR)
    writeWord = self._set_bits(readWord, SI4703_TEST1_XOSCEN_EN, SI4703_TEST1_XOSCEN_MASK, SI4703_TEST1_XOSCEN_LSB)
    self._write_one_reg(SI4703_TEST1_ADDR, writeWord)
  
  def _enable_error_checking(self):
    # set RDSD to 0x0000
    readWord  = self._read_one_reg(SI4703_RDSD_ADDR)
    writeWord = self._set_bits(readWord, 0x0000, SI4703_RDSD_MASK, SI4703_RDSD_BLERB_LSB)
    self._write_one_reg(SI4703_RDSD_ADDR, writeWord)
  
  def _enable_device(self):
    # set ENABLE bit and clear DISABLE bit in Power Configuration Register
    readWord  = self._read_one_reg(SI4703_POWER_CONFIG_ADDR)
    # set ENABLE bit
    writeWord = self._set_bits(readWord, SI4703_POWER_CONFIG_ENABLE_HIGH, SI4703_POWER_CONFIG_ENABLE_MASK, SI4703_POWER_CONFIG_ENABLE_LSB)
    # clear DISABLE bit
    writeWord = self._set_bits(writeWord, SI4703_POWER_CONFIG_DISABLE_LOW, SI4703_POWER_CONFIG_DISABLE_MASK, SI4703_POWER_CONFIG_DISABLE_LSB)
    self._write_one_reg(SI4703_POWER_CONFIG_ADDR, writeWord)
  
  def _led_on(self):
    # set GPIO1 bits = 11 in System Configuration Register 1
    readWord  = self._read_one_reg(SI4703_SYS_CONFIG1_ADDR)
    writeWord = self._set_bits(readWord, SI4703_SYS_CONFIG1_GPIO1_HIGH, SI4703_SYS_CONFIG1_GPIO1_MASK, SI4703_SYS_CONFIG1_GPIO1_LSB)
    self._write_one_reg(SI4703_SYS_CONFIG1_ADDR, writeWord)
  
  def _general_configuration(self):
    # Stereo / Mono blend level, use default value
    # Software attenuation, use default value, 16dB, fastest
    # Volume range, use default value, -28 ~ 0
    # Threshold setting, use recommended value, SEEKTH = 0x19, SKSNR = 0x4, SKCNT = 0x8
    self._sync_read_reg()
    sysConfigWord2 = self._read_one_reg(SI4703_SYS_CONFIG2_ADDR)
    sysConfigWord3 = self._read_one_reg(SI4703_SYS_CONFIG3_ADDR)
    sysConfigWord2 = self._set_bits(sysConfigWord2, SI4703_SYS_CONFIG2_SEEKTH_RECOMMENDED, SI4703_SYS_CONFIG2_SEEKTH_MASK, SI4703_SYS_CONFIG2_SEEKTH_LSB)
    sysConfigWord3 = self._set_bits(sysConfigWord3, SI4703_SYS_CONFIG3_SKSNR_RECOMMENDED, SI4703_SYS_CONFIG3_SKSNR_MASK, SI4703_SYS_CONFIG3_SKSNR_LSB)
    sysConfigWord3 = self._set_bits(sysConfigWord3, SI4703_SYS_CONFIG3_SKCNT_RECOMMENDED, SI4703_SYS_CONFIG3_SKCNT_MASK, SI4703_SYS_CONFIG3_SKCNT_LSB)
    self._write_one_reg(SI4703_SYS_CONFIG3_ADDR, sysConfigWord3)
    self._write_one_reg(SI4703_SYS_CONFIG2_ADDR, sysConfigWord2)
    self._write_sync()

  def _regional_configuration(self, region):
    # Setting band, space, and de-emphasis
    bandVal  = SI4703_BAND_DIC[region]
    spaceVal = SI4703_SPACE_DIC[region]
    DEVal    = SI4703_DE_DIC[region]
    self._sync_read_reg()
    sysConfigWord1 = self._read_one_reg(SI4703_SYS_CONFIG1_ADDR)
    sysConfigWord2 = self._read_one_reg(SI4703_SYS_CONFIG2_ADDR)
    sysConfigWord1 = self._set_bits(sysConfigWord1, DEVal, SI4703_SYS_CONFIG1_DE_MASK, SI4703_SYS_CONFIG1_DE_LSB)
    sysConfigWord2 = self._set_bits(sysConfigWord2, bandVal, SI4703_SYS_CONFIG2_BAND_MASK, SI4703_SYS_CONFIG2_BAND_LSB)
    sysConfigWord2 = self._set_bits(sysConfigWord2, spaceVal, SI4703_SYS_CONFIG2_SPACE_MASK, SI4703_SYS_CONFIG2_SPACE_LSB)
    self._write_one_reg(SI4703_SYS_CONFIG1_ADDR, sysConfigWord1)
    self._write_one_reg(SI4703_SYS_CONFIG2_ADDR, sysConfigWord2)
    self._write_sync()  

  def power_up(self):
    self._id_check()
    self._enable_oscillator()
    self._enable_error_checking()
    self._enable_device()
    self._led_on()
    self._write_sync()
    # wait for 500 ms until oscillator becomes stable
    time.sleep(0.5)    
    self._sync_read_reg()
    chipIDWordData = self._read_one_reg(SI4703_CHIP_ID_ADDR)
    chipDeviceID   = self._extract_bits(chipIDWordData,   SI4703_CHIP_ID_DEV_MASK,      SI4703_CHIP_ID_DEV_LSB      ) 
    chipFirmware   = self._extract_bits(chipIDWordData,   SI4703_CHIP_ID_FIRMWARE_MASK, SI4703_CHIP_ID_FIRMWARE_LSB ) 
    if (chipDeviceID != SI4703_CHIP_ID_DEV_AFTER_UP):
      sys.stderr.write('power up failed, chip DEV ID unmatch, read out value: {}\n'.format(chipDeviceID))
      sys.exit(-1)
    if (chipFirmware != SI4703_CHIP_ID_FIRMWARE_AFTER_UP):
      sys.stderr.write('power up failed, chip Firmware ID unmatch, read out value: {}\n'.format(chipFirmware))
      sys.exit(-1)
    print ("Power up succeeds!")

  def config(self, region = 'USA'):
    if(not region in SI4703_REGION_LIST):
      sys.stderr.write('Region not supported, support region:{}\n'.format(SI4703_REGION_LIST))
      sys.exit(-1)
    self._general_configuration()
    self._regional_configuration(region)
    print ("Config succeeds!")
  
try:
  GPIO.setmode(GPIO.BCM)
  ctrl = SI4703Controller(5,13,2)
  ctrl.power_up()
  ctrl.config('USA')
  while True:
    pass
  
except:
  pass

GPIO.cleanup()
