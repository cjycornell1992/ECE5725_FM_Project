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
import mmap
import struct
import math

class Transmitter:

  def __init__(self, carrier_freq):
    self.peripheral  = None
    self.carrierFreq = carrier_freq
  
  def init(self):
    try:
      memf = open("/dev/mem", "r+b")
      self.peripheral = mmap.mmap(memf.fileno(), PERIPHERAL_LEN, offset = PERIPHERAL_BASE)
      self._setupGPIO()
      self._setupCLK0()
      self._setupCarrier(self.carrierFreq)
      
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
  
  def close(self):
    self.peripheral.close()
