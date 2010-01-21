import pygame
from pygame.locals import *
import random

class Alien(pygame.sprite.Sprite):  
  def __init__(self, coords):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("assets/alien.png")
    self.image.convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.topleft = coords
    self.exploded = 0
  def update(self, speed, width, height):
    if self.exploded:
      self.rect = self.rect.move((-2,1))
      if self.rect.top >= height or self.rect.right <= 0:
        self.kill()
    else:
      self.rect = self.rect.move(speed)
    if self.rect.right <= 0:
      self.rect.top = random.random() * height
      self.rect.left = width
  def explode(self):
    old_bottomleft = self.rect.bottomleft
    self.image = pygame.image.load("assets/alien_on_fire.png")
    self.image.convert_alpha()
    self.rect = self.image.get_rect(bottomleft=(old_bottomleft))
    self.exploded = 1
  #def repair(self):
  #  old_bottomleft = self.rect.bottomleft
  #  self.image = pygame.image.load("assets/alien.png")
  #  self.image.convert_alpha()
  #  self.rect = self.image.get_rect(bottomleft=(old_bottomleft))
  #  self.exploded = 0