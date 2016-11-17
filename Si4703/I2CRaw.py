#################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.16 2016
#
# I2CRaw.py
#
# Description: simple I2C library to manipulate raw I2C file descriptor
#
# __init__:
#   device_addr: i2c address of the i2c device
#   bus: pi-2, device is /dev/i2c-1, so bus value should be 1
#
# write_i2c_block_data:
#   data: data you want to write into i2c device
#   ,note data need to be passed as a list, not tuple, not bytearray
#
# read_i2c_block_data:
#   n_bytes: number of bytes you want to read
#   ,note data will be returned as a list
#
# Reference: https://www.raspberrypi.org/forums/viewtopic.php?t=162248&p=1049717
################################################################

import io
import fcntl
import struct

I2C_SLAVE = 0x0703

class I2CRaw:
  
  def __init__(self, device_addr, bus):
    self.fr = io.open("/dev/i2c-"+str(bus),"rb",buffering = 0)
    self.fw = io.open("/dev/i2c-"+str(bus),"wb",buffering = 0)
    fcntl.ioctl(self.fr, I2C_SLAVE, device_addr)
    fcntl.ioctl(self.fw, I2C_SLAVE, device_addr)
    
  def write_i2c_block_data(self, data):
    if type(data) is not list:
	  return -1
    data = bytearray(data)
    self.fw.write(data)
    return 0
    
  def read_i2c_block_data(self, n_bytes):
    data_raw      = self.fr.read(n_bytes)
    unpack_format = 'B'*n_bytes
    return list(struct.unpack(unpack_format,data_raw))
  
  def close(self):
    self.fr.close()
    self.fw.close()
