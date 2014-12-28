import pygame
from pygame.locals import *

from animation import Animation

class Hero(object):

    def __init__(self, sprites, pos):

        self.animation = Animation(sprites, rate=5)
        self.size = self.animation.get_sprite().get_size()

        self.x, self.y = pos
        self.rect = pygame.Rect(pos, self.size)

    def update(self):
        self.animation.update()

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.animation.get_sprite(), self.rect.topleft

