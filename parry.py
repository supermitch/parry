#!/usr/bin/env python
from __future__ import division
import random
import sys

import pygame
from pygame.locals import *
from pygame import Color

from classes import world
from classes import renderer
from classes import assetloader

class Game(object):
    """
    Primary game object.
    Not sure this is the best way, saw it in someone's game.

    """

    def __init__(self):
        """ Initalize some game constants. """

        self.FPS = 60

        self.width, self.height = 400, 300
        self.size = (self.width, self.height)

        self.renderer = renderer.Renderer(self.size)
        self.assets = assetloader.AssetLoader()
        self.world = world.World(self.size, self.assets)
        self.renderer.world = self.world

    def run(self):
        """Run the actual game."""

        clock = pygame.time.Clock()  # Initialize framerate clock

        while True:  # Game loop

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key in (K_q, K_ESCAPE):
                        terminate()
                    elif event.key == K_a:
                        pass
                    elif event.key == K_s:
                        pass
                    elif event.key == K_s:
                        pass
                    elif event.key == K_d:
                        pass
                    elif event.key == K_SPACE:
                        pass

            self.world.update()
            self.renderer.render()
            clock.tick(self.FPS)


def terminate():
    """ Stop game correct. """
    pygame.quit()   # uninitialize
    sys.exit("Goodbye.")

def main():
    """ Run the game. """
    pygame.init()   # Initialize pygame
    app = Game()  # Instantiate new app
    app.run()
    terminate()

if __name__ == "__main__":
    main()

