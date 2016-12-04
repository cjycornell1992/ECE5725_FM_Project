#################################################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.29 2016
#
# TransmitterTest.py
#
# Description: a simple script to test Transmitter methods
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
import time
import sys
import glob
sys.path.append("..")
from Transmitter.Transmitter import Transmitter
from threading               import Thread

main2Trans_fifo = "main2Trans_fifo"
Trans2main_fifo = "Trans2main_fifo"
script_on       = True

def FIFOReceiveHandler():
  while True:
    global playList
    global music_id
    receive_fifo = open(main2Trans_fifo, "r", buffering = 0)  
    operation = receive_fifo.readline()
    receive_fifo.close()
    if  (operation == "next"):
      move("next")
    elif(operation == "prev"):
      move("prev")
    elif(operation == "pause"):
      transmitter.pause()
    elif(operation == "resume"):
      sender    = Thread(target = FIFOSenderHandler, args = (playList[music_id], ))
      sender.start()
      transmitter.resume()
    elif(operation == "exit"):
      global script_on
      script_on = False
      break
    else:
      print "error, invalid FIFO operation:{}".format(operation)

FIFOReceiveCollector = Thread(target = FIFOReceiveHandler)
FIFOReceiveCollector.start()

playList = glob.glob('../Transmitter/wav/*.wav')

music_id = 0
transmitter = Transmitter(100.0, playList[music_id])
transmitter.init()
transmitter.reader.stat()
transmitter.transmit()
transmitter.pause()

def FIFOSenderHandler(filepath):
  send_fifo = open(Trans2main_fifo, "w", buffering = 0)
  send_fifo.write(filepath)
  send_fifo.close()
  

def move(direction):
  global transmitter
  global music_id
  global playList
  transmitter.stop()
  time.sleep(0.1)
  increment = 1 if direction == "next" else -1
  music_id  = (music_id + increment) % len(playList)
  transmitter.newJob(playList[music_id])
  transmitter.reader.stat()
  transmitter.transmit()
  sender    = Thread(target = FIFOSenderHandler, args = (playList[music_id], ))
  sender.start()

while script_on:
  try:
    while transmitter.busy:
      time.sleep(1)
    if transmitter.reader.isEnd():
      move("next")
  except KeyboardInterrupt:
    fifo = open(main2Trans_fifo, "w", buffering = 0)
    fifo.write("exit")
    fifo.close()
    time.sleep(1)
    break
  
transmitter.close()
