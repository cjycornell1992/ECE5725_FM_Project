#################################################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.27 2016
#
# WaveHeaderConstants.py
#
# Description: This file contains constants to describe the header of a PCM Wave File
#
# Reference:
# 1. http://soundfile.sapp.org/doc/WaveFormat/
# 2.
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

#################################################################################################
###                                   Chunk Descriptor                                        ###
#################################################################################################

# size and offset 
CHUNK_DESCRIPTOR_SIZE            = 12
CHUNK_ID_OFFSET                  = 0
CHUNK_SIZE_OFFSET                = 4
CHUNK_FORMAT_OFFSET              = 8
# constants
PCM_WAVE_CHUNK_ID                = "RIFF"
PCM_WAVE_FORMAT                  = "WAVE"

#################################################################################################
###                                       Subchunk 1                                          ###
#################################################################################################

# size and offset 
SUBCHUNK1_SIZE                   = 24
SUBCHUNK1_ID_OFFSET              = 0
SUBCHUNK1_SIZE_OFFSET            = 4
SUBCHUNK1_AUDIO_FMT_OFFSET       = 8
SUBCHUNK1_NUM_CHANS_OFFSET       = 10
SUBCHUNK1_SAMPLE_RATE_OFFSET     = 12
SUBCHUNK1_BYTE_RATE_OFFSET       = 16
SUBCHUNK1_BLOCK_ALIGN_OFFSET     = 20
SUBCHUNK1_BITS_PER_SAMPLE_OFFSET = 22
# constants
PCM_SUBCHUNK1_ID                 = "fmt "
PCM_SUBCHUNK1_SIZE               = 16
PCM_AUDIO_FORMAT                 = 1

#################################################################################################
###                                       Subchunk 2                                          ###
#################################################################################################

# size and offset
SUBCHUNK2_META_SIZE              = 8
SUBCHUNK2_ID_OFFSET              = 0
SUBCHUNK2_SIZE_OFFSET            = 4 
# constants
PCM_SUBCHUNK2_ID                 = "data"
