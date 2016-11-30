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
  Get one sample from the wave file, No parameter is explicitly passed in, but below are fields serve
  as input, and you might find that useful:
  
  self.wavFile ---- The file descriptor of the file, you can do self.wavFile.read(N) to read N bytes of data out
  the data read out is in str raw data, you need to unpack that. Read python struct pack/unpack for more infomation
  https://docs.python.org/2/library/struct.html
  
  self.dataBlockSize ---- The current size (in bytes) of the audio data still unread in the file. REMEMBER to UPDATE
  THIS FIELD after you get one sample of the audio data

  self.getFormatSummerizer() ---- This gives a summarizer about the format of the audio file. See FormatSummerizer class
  for more information.

  For each sample, you might need to process 1 ~ 4 byte, depending on the format of the audio, format summerizer block align field
  tells you how many bytes you need to read for each sample (including all channels). You need to consider the following 4 cases:
  single channel, 8 bit per sample
  double channel, 8 bit per sample
  single channel, 16 bit per sample
  double channel, 16 bit per sample
  Number of channels and bits/sample could be found in the format summerizer class
  data packing for the above 4 cases could be found at http://www.neurophys.wisc.edu/auditory/riff-format.txt

  After reading corresponding bits out, scale that to 0 ~ 1

  Example: single channel, 8 bit per sample, read one byte out, unpack, found this is 127, because one byte is 0 ~ 255, this value
  should be 127/255, return 0.5

  For double channels, remember to take the average value.

  For 16-bit number, remember to add a DC offset to the signed integer so -32768 ~ 32767 gets converted to 0 ~ 1 instead of -1 ~ 1.

  Example: -32768 should not be scaled to 1, it should be scaled to 0. 0 should not be scaled to 0, it should be scaled to 0.5

  return: a float number 0 ~ 1 that is the scaled data of one sample  

  """
  def getOneSample(self):
    # Zhenchuan TODO
  	pass

  """
  Deciding If you can still read at least one more sample. Again, this has no input parameter, but you might want to modify following fields:

  self.dataBlockSize --- The current number of data still unread, in bytes
  blockalign field in the format summerizer, this tells you how many bytes per sample (includig all channels)
  
  Return:
  True  if current dataBlockSize is less than one sample
  False if you can still read at least one sample
  """
  def isEnd(self):
  	# Zhenchuan TODO
  	pass

  """
  Skip number of samples in the file
  
  Input: num_samples

  Fields might be useful:
  self.wavFile ---- The file descriptor of wav file. Use tell / seek to do that. https://docs.python.org/2/tutorial/inputoutput.html

  self.dataBlockSize ---- Remember to update this field after skip several samples

  return
  True  if you can skip this number of samples, and it succeeds
  False if the num of sample you want to skip exceeds the current data block size
  """
  def skipSamples(self, num_samples):
  	# Zhenchuan TODO
  	pass

