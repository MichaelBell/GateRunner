#!/usr/bin/env python
#
# Gate runner for UnicornHat.
# Control with WASD, and change colour with shift and control
# Q to quit.
#
# If you have the right bits around, control with a Wii Nunchuck with:
# https://github.com/MichaelBell/MinimusChuck

import unicornhat
import pygame
import time
import sys
import random

def pixel(pos, col, brightness=1.0):
  col = [int(c*brightness) for c in col]
  unicornhat.set_pixel(pos[0], pos[1], col[0], col[1], col[2])

def fill(col):
  for i in xrange(8):
    for j in xrange(8):
      pixel((i,j), col)

red = (220,0,0)
green = (0,220,0)
blue = (0,0,255)
purple = (140, 0, 220)
white = (220,220,220)
black = (0,0,0)
brown = (90,80,40)

size = [640,480]

class game:
  def __init__(self):
    self.gate_cols = (red, green, blue, purple)
    self.reset()

  def reset(self):
    self.gate = [3, 7, red]
    self.failed = False
    self.speed = 50
    self.frame = 0
    self.level = 1
  
  def update(self, p, col, frame):
    if self.failed:
      if frame > self.frame + self.speed:
        fill(black)
        self.reset()
      return

    if (frame > self.frame + self.speed):
      self.frame = frame
      for i in xrange(8):
        pixel((i,self.gate[1]), black)
      self.gate[1] = self.gate[1] - 1
      if self.gate[1] == -1:
        self.gate[0] = random.randint(0,7)
        self.gate[1] = 7
        self.gate[2] = random.choice(self.gate_cols[0:self.level])
        self.speed = self.speed - 1
        if self.speed == 30 and self.level < 4:
          self.level = self.level + 1
          self.speed = 45
      for i in xrange(8):
        pixel((i,self.gate[1]), white)
      pixel(self.gate[0:2], self.gate[2], 0.7)
    if self.gate[1] == p[1]:
      if self.gate[0] != p[0] or col != self.gate[2]:
        self.failed = True
        self.speed = 200
        fill(red)

def main():
  pygame.display.init()
  screen = pygame.display.set_mode(size)
  clock = pygame.time.Clock()
  unicornhat.brightness(0.15)

  pygame.key.set_repeat(100, 100)

  frame = 0
  p = [3,0]
  newp = [3,0]
  g = game()

  pixel(p, red)

  done = False
  while not done:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
          newp[0] = min(p[0] + 1, 7)
        if event.key == pygame.K_d:
          newp[0] = max(p[0] - 1, 0)
        if event.key == pygame.K_w:
          newp[1] = min(p[1] + 1, 7)
        if event.key == pygame.K_s:
          newp[1] = max(p[1] - 1, 0)
        if event.key == pygame.K_q:
          pygame.event.post(pygame.event.Event(pygame.QUIT))
    mods = pygame.key.get_mods()
    col = red
    if mods & pygame.KMOD_SHIFT: 
      if mods & pygame.KMOD_CTRL: col = purple
      else: col = green
    elif mods & pygame.KMOD_CTRL: col = blue

    frame = frame + 1
    g.update(newp, col, frame)

    pixel(p, black)
    pixel(newp, col)
    p = [a for a in newp]
    unicornhat.show()
    screen.fill(black)
    pygame.display.update()
    clock.tick(100)

  pygame.quit()

if __name__ == '__main__':
  main()
