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
    self.filename      = filename
    self.wavFile       = None
    self.header        = None
    self.dataBlockSize = 0

  def init(self):
    try:
      self.wavFile = open(self.filename, "rb")
      self._getPCMWaveHeader()
      self.dataBlockSize = self.header.subchunk2Size

    except IOError, error:
      print "IOError : {}".format(error)
      raise WaveReaderException("Error in wave reader initialization")

  def close(self):
    try:
      self.wavFile.close()
    except:
      raise WaveReaderException("Error: unable to close the wav file")

  def stat(self):
    print "Now Playing: {}".format(self.filename)
    self.header.stat()
    print "Data Block Size: {} KB".format(self.dataBlockSize >> 10)

  def getFormatSummerizer(self):
    return self.header.getFormatSummerizer()

  def _getPCMWaveHeader(self):
    self.header = PCMWaveHeader()
    # chunk descriptor get & check
    self._getChunkDescriptor()
    self._checkChunkDescriptor()
    # subchunk1 get & check
    self._getSubchunk1()
    self._checkSubchunk1()
    # subchunk2 get & check
    self._getSubchunk2()
    self._checkSubchunk2()
    self.header._setFormatSummerizer()    

  def _getChunkDescriptor(self):
    try:
      chunkData = self.wavFile.read(CHUNK_DESCRIPTOR_SIZE)
      self.header.chunkID    = chunkData[CHUNK_ID_OFFSET : CHUNK_SIZE_OFFSET]
      # numbers are little endian
      self.header.chunkSize  = struct.unpack('<I', chunkData[CHUNK_SIZE_OFFSET : CHUNK_FORMAT_OFFSET])[0]
      self.header.format     = chunkData[CHUNK_FORMAT_OFFSET : CHUNK_DESCRIPTOR_SIZE]
    except:
      raise WaveReaderException("Error: unable to get chunk descriptor")

  def _checkChunkDescriptor(self):
    if(self.header.chunkID != PCM_WAVE_CHUNK_ID):
      raise WaveReaderException("Error: Header does not begin with RIFF")
    if(self.header.format  != PCM_WAVE_FORMAT):
      raise WaveReaderException("Error: Format not WAVE, unsupported")

  def _getSubchunk1(self):
    try:
      subchunk1Data = self.wavFile.read(SUBCHUNK1_SIZE)
      self.header.subchunk1ID   = subchunk1Data[SUBCHUNK1_ID_OFFSET : SUBCHUNK1_SIZE_OFFSET]
      self.header.subchunk1Size = struct.unpack('<I', subchunk1Data[SUBCHUNK1_SIZE_OFFSET            : SUBCHUNK1_AUDIO_FMT_OFFSET])[0]
      self.header.audioFormat   = struct.unpack('<H', subchunk1Data[SUBCHUNK1_AUDIO_FMT_OFFSET       : SUBCHUNK1_NUM_CHANS_OFFSET])[0]
      self.header.numChannels   = struct.unpack('<H', subchunk1Data[SUBCHUNK1_NUM_CHANS_OFFSET       : SUBCHUNK1_SAMPLE_RATE_OFFSET])[0]
      self.header.sampleRate    = struct.unpack('<I', subchunk1Data[SUBCHUNK1_SAMPLE_RATE_OFFSET     : SUBCHUNK1_BYTE_RATE_OFFSET])[0]
      self.header.byteRate      = struct.unpack('<I', subchunk1Data[SUBCHUNK1_BYTE_RATE_OFFSET       : SUBCHUNK1_BLOCK_ALIGN_OFFSET])[0]
      self.header.blockAlign    = struct.unpack('<H', subchunk1Data[SUBCHUNK1_BLOCK_ALIGN_OFFSET     : SUBCHUNK1_BITS_PER_SAMPLE_OFFSET])[0]
      self.header.bitsPerSample = struct.unpack('<H', subchunk1Data[SUBCHUNK1_BITS_PER_SAMPLE_OFFSET : SUBCHUNK1_SIZE])[0]
    except:
      raise WaveReaderException("Error: unable to get subchunk 1")

  def _checkSubchunk1(self):
    if(self.header.subchunk1ID   != PCM_SUBCHUNK1_ID):
      raise WaveReaderException("Error: subchunk1 does not begin with fmt ")
    if(self.header.subchunk1Size != PCM_SUBCHUNK1_SIZE or self.header.audioFormat != PCM_AUDIO_FORMAT):
      raise WaveReaderException("Error: not PCM format, unsupported")
    if(self.header.numChannels != 1 and self.header.numChannels != 2):
      raise WaveReaderException("Error: more than 2 channels, unsupported format")

  def _getSubchunk2(self):
    try:
      subchunk2Data = self.wavFile.read(SUBCHUNK2_META_SIZE)
      self.header.subchunk2ID   = subchunk2Data[SUBCHUNK2_ID_OFFSET : SUBCHUNK2_SIZE_OFFSET]
      self.header.subchunk2Size = struct.unpack('<I', subchunk2Data[SUBCHUNK2_SIZE_OFFSET : SUBCHUNK2_META_SIZE])[0]
    except:
      raise WaveReaderException("Error: unable to get subchunk 2 meta data")

  def _checkSubchunk2(self):
    if(self.header.subchunk2ID != PCM_SUBCHUNK2_ID):
      raise WaveReaderException("Error: subchunk2 does not begin with data")


  """
  Get one sample from the wave file
  
  self.wavFile ---- The file descriptor of the file
  self.dataBlockSize ---- The current size (in bytes) of the audio data still unread in the file. UPDATED Here

  deal with the following 4 cases:
  single channel, 8 bit per sample
  double channel, 8 bit per sample
  single channel, 16 bit per sample
  double channel, 16 bit per sample

  Reference: http://www.neurophys.wisc.edu/auditory/riff-format.txt
  
  After reading corresponding bits out, scale that to 0 ~ 1

  return: a float number 0 ~ 1 that is the scaled data of one sample  

  """
  def getOneSample(self):
    if self.isEnd():
      raise WaveReaderException("Error in getOneSample: remained data size not enough for one sample")
    formatSummerizer = self.getFormatSummerizer()
    bytePerSample = formatSummerizer.blockAlign
    bitsPerSampleOneChannel = formatSummerizer.bitsPerSample
    channelNum = formatSummerizer.numChannels
    content = self.wavFile.read(bytePerSample)
    self.dataBlockSize -= bytePerSample
    val = 0
    if bitsPerSampleOneChannel == 8:
        if channelNum == 1:
            # 8 bit, 1 channel
            val = struct.unpack('B', content)[0]
            val = val / 255.0
        else:
            # 16 bit in total, 2 channels, each 8 bits
            val = struct.unpack('B', content)
            c0 = val[0] >> 1
            c1 = val[1] >> 1
            val = (c0 + c1) / 255.0 
    else:
        if channelNum == 1:
			# 16 bit, 1 channel
			# content[0]: low byte; content[1]: high byte; can use unpack directly
            val = struct.unpack('<h', content)[0]
            #val = (val + 32768.0) / (32767 * 2.0)
            val = (val + 32768.0) / float(32767 << 1)
        else:
			# 32 bits total, 2 channel
			# first 16 bits for sample 1, second 16 bits for sample 2, little endian
            val0, val1 = struct.unpack('<hh', content)
            #val = (((val0 + val1) / 2.0) + 32768.0) / (32767 * 2.0)
            val = (((val0 >> 2) + (val1 >> 2)) + (32768 >> 1)) / float(32767)           
    return val
  	  	
  """
  Deciding If you can still read at least one more sample.
  
  Return:
  True  if current dataBlockSize is less than one sample
  False if you can still read at least one sample
  """
  def isEnd(self):
    formatSummerizer = self.getFormatSummerizer()
    bytePerSample = formatSummerizer.blockAlign
    return self.dataBlockSize < bytePerSample

  """
  Skip number of samples in the file
  
  Input: num_samples

  self.wavFile ---- The file descriptor of wav file. 
  self.dataBlockSize ---- update this field after skip several samples

  return
  True  if you can skip this number of samples, and it succeeds
  False if the num of sample you want to skip exceeds the current data block size
  """
  def skipTo(self, dest_sample_index):
    formatSummerizer = self.getFormatSummerizer()
    bytePerSample = formatSummerizer.blockAlign
    if self.dataBlockSize < bytePerSample * num_samples:
        return False    
    cur = self.wavFile.tell()
    des = cur + bytePerSample * num_samples
    self.wavFile.seek(des)
    self.dataBlockSize -= bytePerSample * num_samples
    return True

