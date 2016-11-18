import pygame
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
    button = GUIButton(text, pos, size, color, call_back)
    self.buttons.append(button)


