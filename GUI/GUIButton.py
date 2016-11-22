#################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.22 2016
#
# GUIButton.py
#
# Description: This GUI library is based on pygame framework
# Button class knows its own text, its own position on the screen,
# And bundles a callback (could be None, though) that should be called
# when the button is pressed. The user could also add extra callbacks
# if the user wants to extend the ability of a button in the future
#              
################################################################

import pygame

class GUIButton:
  
  def __init__(self, page, text, pos, size, color, call_back):
    self.font          = pygame.font.Font(None, size)
    self.page          = page
    self.text          = text
    self.pos           = pos
    self.color         = color
    self.surface       = self.font.render(self.text, True, color)
    self.rect          = self.surface.get_rect(center = self.pos)
    self.left          = self.rect.left
    self.right         = self.rect.right
    self.top           = self.rect.top
    self.bottom        = self.rect.bottom
    self.callBack      = call_back
    self.extraCallBack = None

  def update_text(self, text):
    self.text = text

  def extra_callback(self, call_back):
    self.extraCallBack = call_back
