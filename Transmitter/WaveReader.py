#################################################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.27 2016
#
# WaveReader.py
#
# Description: simple WaveReader Library to provide basic handling
# and decoding methods for wav file
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

from WaveReaderException import WaveReaderException
from PCMWaveHeader       import PCMWaveHeader
from WaveHeaderConstants import *
import struct

class WaveReader:
  
  def __init__(self, filename):
    self.filename = filename
    self.wavFile  = None
    self.header   = None

  def init(self):
    try:
      self.wavFile = open(self.filename, "rb")
      self._getPCMWaveHeader()

    except IOError, error:
      print "IOError : {}".format(error)
      raise WaveReaderException("Error in wave reader initialization")

  def close(self):
    try:
      self.wavFile.close()
    except:
      raise WaveReaderException("Error: unable to close the wav file")

  def _getPCMWaveHeader(self):
    self.header = PCMWaveHeader()
    self._getChunkDescriptor()
    self._checkChunkDescriptor()
    self.header.stat()

  def _getChunkDescriptor(self):
    try:
      chunkData = self.wavFile.read(CHUNK_DESCRIPTOR_SIZE)
      self.header.chunkID    = chunkData[CHUNK_ID_OFFSET:CHUNK_SIZE_OFFSET]
      # numbers are little endian
      self.header.chunkSize = struct.unpack('<I', chunkData[CHUNK_SIZE_OFFSET:CHUNK_FORMAT_OFFSET])[0]
      self.header.format     = chunkData[CHUNK_FORMAT_OFFSET:CHUNK_DESCRIPTOR_SIZE]
    except:
      raise WaveReaderException("Error: unable to get chunk descriptor")

  def _checkChunkDescriptor(self):
    if(self.header.chunkID != PCM_WAVE_CHUNK_ID):
      raise WaveReaderException("Error: Header does not begin with RIFF")
    if(self.header.format != PCM_WAVE_FORMAT):
      raise WaveReaderException("Error: Format not WAVE, unsupported")



