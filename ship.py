import pygame
from pygame.locals import *

class Ship(pygame.sprite.Sprite):
  def __init__(self, coords):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("assets/ship.png")
    self.image.convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.topleft = coords
  def update(self, speed, width, height):
    if (self.rect.left + speed[0]) < 0 or (self.rect.right + speed[0]) > width:
      speed[0] = 0
    if (self.rect.top + speed[1]) < 0 or (self.rect.bottom + speed[1]) > height:
      speed[1] = 0        
    self.rect = self.rect.move(speed)