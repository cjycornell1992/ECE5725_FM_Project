import pygame

class GUIButton:
  
  def __init__(self, page, text, pos, size, color, call_back):
    self.font     = pygame.font.Font(None, size)
    self.page     = page
    self.text     = text
    self.pos      = pos
    self.color    = color
    self.surface  = self.font.render(self.text, True, color)
    self.rect     = self.surface.get_rect(center = self.pos)
    self.left     = self.rect.left
    self.right    = self.rect.right
    self.top      = self.rect.top
    self.bottom   = self.rect.bottom
    self.callBack = call_back

  def update_text(self, text):
    self.text = text
 
