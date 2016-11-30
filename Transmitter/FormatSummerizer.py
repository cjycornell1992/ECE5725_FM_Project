#################################################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.28 2016
#
# FormatSummerizer.py
#
# Description: This class is for summerizing the format of a given wav file
# number of channels, bits/sample and sample rate are 3 key data that are visited
# frequently in applications.
#
# Reference:
# 
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

class FormatSummerizer:

  def __init__(self, channel_num, bits_per_sample, sample_rate, block_align):
  	self.numChannels   = channel_num
  	self.bitsPerSample = bits_per_sample
  	self.sampleRate    = sample_rate
    self.blockAlign    = block_align