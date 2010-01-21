#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/2.5/bin/python
# encoding: utf-8
"""
sfaopdq.py

Created by Tom Quackenbush on 2009-06-24.
"""

import sys
import os
import random
import time
import pygame
from pygame.locals import *
from ship import Ship
from shot import Shot
from alien import Alien
from stats import Stats

pygame.init()

size = width, height = 640, 480
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
font = pygame.font.Font(None, 17)

ship = pygame.sprite.GroupSingle(Ship([0,0]))
shots = pygame.sprite.Group()
aliens = pygame.sprite.Group()
aliens_exploded = pygame.sprite.Group()

aliens.add(Alien([width, random.random() * height]))

exploded = 0

# stats...
stats = Stats()
stats.metrics["start_time"] = pygame.time.get_ticks()
stats.metrics["shots_fired"] = 0
stats.metrics["aliens_hit"] = 0

while not exploded:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYUP:
          pressed_keys = pygame.key.get_pressed()
          if not (pressed_keys[K_UP] or pressed_keys[K_DOWN]):
            speed[1] = 0
          if not (pressed_keys[K_RIGHT] or pressed_keys[K_LEFT]):
            speed[0] = 0
        if event.type == pygame.KEYDOWN:
          pressed_keys = pygame.key.get_pressed()
          if (pressed_keys[K_UP] or pressed_keys[K_DOWN] or pressed_keys[K_RIGHT] or pressed_keys[K_LEFT]):
            speed = [0,0]
            if pressed_keys[K_UP] and (not pressed_keys[K_DOWN] or (pressed_keys[K_DOWN] and event.key == K_UP)):
              speed[1] = -2
            if pressed_keys[K_DOWN] and (not pressed_keys[K_UP] or (pressed_keys[K_UP] and event.key == K_DOWN)):
              speed[1] = 2
            if pressed_keys[K_RIGHT] and (not pressed_keys[K_LEFT] or (pressed_keys[K_LEFT] and event.key == K_RIGHT)):
              speed[0] = 2
            if pressed_keys[K_LEFT] and (not pressed_keys[K_RIGHT] or (pressed_keys[K_RIGHT] and event.key == K_LEFT)):
              speed[0] = -2
          if pressed_keys[K_SPACE]:
            stats.metrics["shots_fired"] += 1
            shots.add(Shot(ship.sprite.rect.midright))
            aliens.add(Alien([width, random.random() * height]))

    aliens.update([-2,0], width, height)
    aliens_exploded.update([-2,0], width, height)
    shots.update([3,0], width, height)
    ship.update(speed, width, height)

    collisions = pygame.sprite.groupcollide(aliens, shots, 1, 1)
    absorbed_shots = pygame.sprite.groupcollide(aliens_exploded, shots, 0, 1)
    stats.metrics["aliens_hit"] += len(collisions)
    aliens_exploded.add(collisions)
    for alien in collisions.iterkeys():
      alien.explode()

    if pygame.sprite.spritecollideany(ship.sprite, aliens) or pygame.sprite.spritecollideany(ship.sprite, aliens_exploded):
      stats.metrics["end_time"] = pygame.time.get_ticks()
      exploded = 1
            
    play_seconds = (pygame.time.get_ticks() - stats.metrics["start_time"]) / 1000
    timer_text = font.render(time.strftime("%H:%M:%S", time.gmtime(play_seconds)), True, (255, 255, 255))
    timer_textRect = timer_text.get_rect(bottomleft=screen.get_rect().bottomleft)
    
    screen.fill(black)
    shots.draw(screen)
    aliens.draw(screen)
    aliens_exploded.draw(screen)
    ship.draw(screen)
    screen.blit(timer_text, timer_textRect)

    if exploded:
      text = font.render("Shots Fired: " + str(stats.metrics["shots_fired"]) + "  Aliens Hit: " + str(stats.metrics["aliens_hit"]), True, (255, 255, 255), (255, 0, 0))
      textRect = text.get_rect(center=screen.get_rect().center)
      screen.blit(text, textRect)
    
    pygame.display.flip()

    if exploded:
      pygame.time.delay(5000)
