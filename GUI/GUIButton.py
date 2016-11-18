import pygame

class GUIButton:
  
  def __init__(self, text, pos, size, color, call_back):
    self.font     = pygame.font.Font(None, size)
    self.text     = text
    self.pos      = pos
    self.color    = color
    self.surface  = self.font.render(self.text, True, color)
    self.rect     = self.surface.get_rect(center = self.pos)
    self.callBack = call_back
