#################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.22 2016
#
# GUIPageManager.py
#
# Description: This GUI library is based on pygame framework
# Page Manager class knows all pages it has, and knows the current page
# in the page list. Also, it has a switch to enable all the callbacks
# of buttons in all pages. This switch should be enabled after all pages,
# all buttons have been added, and all callbacks have been specified,
# otherwise it might have undefined behaviour. The switch spawns a child
# thread to collect mouse clicks (finger taps) on the screen (touchscreen),
# a user should disable the switch to kill the child thread and ends
# the script., note an exit button is implicitly attached to every page
# clicking the exit button could elegantly end the script
#             
################################################################

import pygame
from GUIPage        import GUIPage
from threading      import Thread
from ColorConstants import *
        
class GUIPageManager:

  def __init__(self, size = (320, 240), debug = False):

    pygame.init()
    pygame.mouse.set_visible(debug)

    self.screen         = pygame.display.set_mode(size)
    self.curPageNum     = 0
    self.curPage        = None
    self.pageNumCount   = 0
    self.pages          = []
    self.pageDic        = {}
    self.on             = False

  def add_page(self):
    page = GUIPage(self, self.pageNumCount)
    if(self.pageNumCount == 0):
      self.curPage = page      
    
    self.pages.append(page)
    self.pageDic[self.pageNumCount] = page
    self.pageNumCount += 1
    return page
    
  def render(self):
    self.screen.fill(BLACK)
    self.curPage._blit()
    pygame.display.flip()

  def _mouse_detect(self):
    while self.on:
      for event in pygame.event.get():
        if (event.type is pygame.MOUSEBUTTONUP):
          pos = pygame.mouse.get_pos()
          x,y = pos
          print 'touch at {},{}'.format(x,y)
          button = self.curPage._get_clicked_button(x,y)
          if button != None:
            if button.callBack != None:
              button.callBack()
            if button.extraCallBack != None:
              button.extraCallBack()
  
  def turn_to_page(self, page, set_parent = True):
    if (page != None) and (page in self.pages):
      if set_parent:
        page.parentNum  = self.curPageNum
      self.curPageNum = page.num
      self.curPage    = page
  
  def control_enable(self):
    self.on        = True
    mouseCollector = Thread(target = self._mouse_detect)
    mouseCollector.start()

  def control_disable(self):
	self.on  = False
 
