import pygame
from GUIButton import GUIButton
from ColorConstants import *

class GUIPage:
  
  def __init__(self, manager, num):
    self.buttons   = []
    self.manager   = manager
    self.num       = num
    self.parentNum = -1
    self._add_exit_button()
  
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

  def _back_callback(self):
    if self.parentNum != -1:
      self.manager.turn_to_page(self.manager.pageDic[self.parentNum], set_parent = False)

  def _add_exit_button(self, pos = (280, 180), size = 40, color = RED):
    button = self.add_button("exit", pos, size, color, self._exit_callback)
    return button

  def add_back_button(self, pos = (280, 210), size = 40, color = CYAN):
    button = self.add_button("back", pos, size, color, self._back_callback)
    return button
