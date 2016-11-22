import pygame
import sys
from GUIButton import GUIButton
from ColorConstants import *

class GUIPage:
  
  def __init__(self, manager, num):
    self.buttons = []
    self.manager = manager
    self.num     = num
  
  def _blit(self):
    for button in self.buttons:
      self.manager.screen.blit(button.surface, button.rect)

  def add_button(self, text, pos, size = 20, color = WHITE, call_back = None):
    button = GUIButton(self, text, pos, size, color, call_back)
    self.buttons.append(button)
    return button

  def _get_clicked_button(self, x, y):
    for button in self.buttons:  
      if x > button.left  and x < button.right and y < button.bottom and y > button.top:
        print "found a click on button"
        return button
    return None    

  def _exit_callback(self):
    self.manager.control_disable()
    print "exiting"
    #raise KeyboardInterrupt
    #sys.exit(0)

  def add_exit(self, pos = (280, 160), size = 40, color = WHITE):
    self.add_button("exit", pos, size, color, self._exit_callback)

 
