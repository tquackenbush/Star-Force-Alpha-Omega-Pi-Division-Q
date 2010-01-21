import pygame
from pygame.locals import *

class Shot(pygame.sprite.Sprite):
  def __init__(self, mid_coords):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("assets/shot.png")
    self.image.convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.midleft = mid_coords
  def update(self, speed, width, height):
    self.rect = self.rect.move(speed)
    if (self.rect.right + speed[0]) <= 0 or (self.rect.left + speed[0]) >= width:
      self.kill()