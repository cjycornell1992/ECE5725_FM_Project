import pygame
import os
from GUIPage        import GUIPage
from threading      import Thread
from ColorConstants import *

def _mouse_detect():
  while True:
    for event in pygame.event.get():
      if (event.type is pygame.MOUSEBUTTONUP):
        pos = pygame.mouse.get_pos()
        x,y = pos
        print 'touch at {},{}'.format(x,y)

class GUIPageManager:

  def __init__(self, size = (320, 240)):
    pygame.init()
    self.screen        = pygame.display.set_mode(size)
    self.curPageNum    = 0
    self.curPage       = None
    self.pageNumCount  = 0
    self.pages         = []
    self.pageDic       = {}
    # self._set_env()
  
  def _set_env(self):
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
    pygame.mouse.set_visible(False)

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
  
  def control_enable(self):
    mouseCollector = Thread(target = _mouse_detect)
    mouseCollector.start()
