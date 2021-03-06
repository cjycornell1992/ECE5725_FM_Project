#################################################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.29 2016
#
# Transmitter.py
#
# Description: Transmitter class to modulate and transmit FM signal
#
# Reference:
"""
    fm_transmitter - use Raspberry Pi as FM transmitter

    Copyright (c) 2015, Marcin Kondej
    All rights reserved.

    See https://github.com/markondej/fm_transmitter

    Redistribution and use in source and binary forms, with or without modification, are
    permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this list
    of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice, this
    list of conditions and the following disclaimer in the documentation and/or other
    materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its contributors may be
    used to endorse or promote products derived from this software without specific
    prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
    EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
    SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
    TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
    BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
    WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
#
#################################################################################################
from BCM2836Constants import *
from WaveReader       import WaveReader
from threading        import Thread
import time
import mmap
import struct
import math

class Transmitter:

  def __init__(self, carrier_freq, filename):
    self.peripheral  = None
    self.carrierFreq = carrier_freq
    self.reader      = WaveReader(filename)
    self.busy        = False
  
  def init(self):
    try:
      memf = open("/dev/mem", "r+b")
      self.peripheral = mmap.mmap(memf.fileno(), PERIPHERAL_LEN, offset = PERIPHERAL_BASE)
      self._setupGPIO()
      self._setupCLK0()
      self._setupCarrier(self.carrierFreq)
      self.reader.init()
      
    except IOError, error:    
      print "IOError : {}".format(error)

  def _setupGPIO(self):
    gpio_reg = self._read32bits(GPFSEL0_BASE)
    gpio_reg = (gpio_reg & GPFSEL0_FSEL4_MASK) | (GPFSEL0_FSEL4_GPCLK0)     
    self._write32bits(GPFSEL0_BASE, gpio_reg)

  def _read32bits(self, base_addr):
    return struct.unpack("<I", self.peripheral[base_addr : base_addr + 4])[0]

  def _write32bits(self, base_addr, data):
    self.peripheral[base_addr : base_addr + 4] = struct.pack("<I", data)

  def _setupCLK0(self):
    clk0_reg = self._read32bits(CM_GP0CTL_BASE)
    clk0_reg = CM_GP0CTL_PASSWD | CM_GP0CTL_MASH_1STAGE | CM_GPOCTL_ENABLE | CM_GP0CTL_SRC_PLLD
    self._write32bits(CM_GP0CTL_BASE, clk0_reg)
  
  def _setupCarrier(self, freq_mhz):
    if (freq_mhz > 108):
      print "freq_mhz exceeds upper bound, set as 108 instead"
      freq_mhz = 108
    elif (freq_mhz < 87.5):
      print "freq_mhz exceeds lower bound, set as 87.5 instead"
      freq_mhz = 87.5
    
    div      = PLLD_FREQ_MHZ / freq_mhz
    div_int  = int(math.floor(div))
    div_frac = div - div_int
    
    frac_sum = 0
    frac_digit = 0x01 << 11
    frac_step = 0.5
    # 0.01 is enough for resolution of .1 MHz assume 500 MHz clock and 100 MHz carrier
    while (div_frac > 0.01):
      frac_sum   += frac_digit
      frac_digit  = frac_digit >> 1
      div_frac   -= frac_step
      frac_step   = frac_step / 2.0
    
    clk0_div_reg = self._read32bits(CM_GP0DIV_BASE)
    clk0_div_reg = CM_GP0DIV_PASSWD | (div_int << CM_GP0DIV_DIVI_LSB) | frac_sum
    self._write32bits(CM_GP0DIV_BASE, clk0_div_reg)
  
  def _setup_deviation(self, value):
    # assume the value is 0 ~ 1.0
    # only use bottom 4 bits of DIVF for the deviation
    # This results in a deviation within 0.2 MHz, good enough for resulotion
    divf = int(value * 16.0)
    if divf > 15.0:
      divf = 15.0
  
    clk0_div_reg = self._read32bits(CM_GP0DIV_BASE)
    clk0_div_reg = (clk0_div_reg & CM_GP0DIV_DIVF_MASK) | CM_GP0DIV_PASSWD | divf
    self._write32bits(CM_GP0DIV_BASE, clk0_div_reg)

  def _getCurrentTime(self):
    return (self._read32bits(SYS_TIMER_HIGH32_BASE) << 32) + self._read32bits(SYS_TIMER_LOW32_BASE)
    
  def transmit(self, force_start_time = 0):
    self.busy  = True
    formatSummerizer = self.reader.getFormatSummerizer()
    sampleRate = formatSummerizer.sampleRate
    startTime  = force_start_time if force_start_time != 0 else self._getCurrentTime()
    modulator  = Thread(target = self._modulate, args = (startTime, sampleRate))
    modulator.start()

  def _modulate(self, start_time, sample_rate):
    while self.busy and not self.reader.isEnd():
      duration    = self._getCurrentTime() - start_time
      # time value is in us
      # duaration in second t = duration / 10^6 us
      # index = t * sampleRate
      sampleIndex = int((duration / 1e6) * sample_rate)
      if self.reader.skipTo(sampleIndex):
        sample    = self.reader.getOneSample()
        self._setup_deviation(sample)
      else:
        self.reader.dataBlockSize = 0
        break
  
    self.busy = False


  """
    update the base frequency of the carrier wave
    input : frequency number, in MHz
    
    note: the frequency is only valid between 87.5 ~ 108
    any frequency greater than 108 would be rounded down to 108
    any frequency less than 87.5 would be rounded up to 87.5
  """
  def updateCarrierFrequency(self, freq_mhz):
    if (freq_mhz > 108):
      self.carrierFreq = 108
    elif (freq_mhz < 87.5):
      self.carrierFreq = 87.5

    self._setupCarrier(freq_mhz)

  """
    start a new transcation
    input: filename
    
    note: please call this job when a previous transcation has ended
          1. you can call stop to force the previous transcation to stop
          2. you can poll self.busy field and wait until the previous transcation naturally ends 
  """
  def newJob(self, filename):
    self.reader = WaveReader(filename)
    self.reader.init()      
  
  """ forcibaly stop the current transcation, not able to resume """
  def stop(self):
    self.busy = False
    # sleep 0.1 second, wait for the exit of modulate thread
    time.sleep(0.1)
    if(self.reader != None):
      self.reader.close()

  """ Pause the current transcation, able to resume """
  def pause(self):
    self.busy = False
    # sleep 0.1 second, wait for the exit of modulate thread
    time.sleep(0.1)
  
  """ resume a paused transcation, resume a running transaction might have undefined behaviour """  
  def resume(self):
    formatSummerizer = self.reader.getFormatSummerizer()
    sampleRate       = formatSummerizer.sampleRate
    sampleConsumed   = self.reader.sampleConsumed()
    # duration in us
    duration         = int((sampleConsumed / float(sampleRate)) * 1e6)
    startTime        = self._getCurrentTime() - duration
    self.transmit(startTime)
  
  """ Close the entire transmitter device, only call this as a cleanup """  
  def close(self):
    self.stop()
    self.peripheral.close()  
