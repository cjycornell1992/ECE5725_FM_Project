import pygame
import os
from GUIPage        import GUIPage
from threading      import Thread
from ColorConstants import *
        
class GUIPageManager:

  def __init__(self, size = (320, 240), debug = False):
    pygame.init()
    self.screen        = pygame.display.set_mode(size)
    self.curPageNum    = 0
    self.curPage       = None
    self.pageNumCount  = 0
    self.pages         = []
    self.pageDic       = {}
    if not debug:
      self._set_env()
  
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

  def _mouse_detect(self):
    while True:
      for event in pygame.event.get():
        if (event.type is pygame.MOUSEBUTTONUP):
          pos = pygame.mouse.get_pos()
          x,y = pos
          print 'touch at {},{}'.format(x,y)
          button = self.curPage._get_clicked_button(x,y)
          if button != None:
            if button.callBack != None:
              button.callBack()
  
  def turn_to_page(self, page):
    if (page != None) and (page in self.pages):
      self.curPage = page
  
  def control_enable(self):
    mouseCollector = Thread(target = self._mouse_detect)
    mouseCollector.start()
