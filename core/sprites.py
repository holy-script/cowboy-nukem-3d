import pygame as pg
from pygame.locals import *
import math
import os
from config import *


class GameSprite(pg.sprite.Sprite):
    def __init__(self, src, screen, point, pos):
        super().__init__()
        self.image = pg.image.load(src).convert_alpha()
        self.rect = self.image.get_rect()
        setattr(self.rect, pos, point)
        self.pos = pos
        self.point = point
        self.screen = screen
        self.cropped = False
        self.crop_area = pg.rect.Rect(0, 0, 0, 0)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        setattr(self.rect, self.pos, self.point)

    def destroy(self):
        self.kill()
