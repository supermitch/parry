import pygame
from pygame.locals import *

class Renderer(object):
    """ Render the world. """

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.surf = pygame.display.set_mode(self.screen_size, RESIZABLE)

        pygame.display.set_caption('Parry 1.0')

        self.BG_COLOR = (255, 0, 255)

        self.text = pygame.font.Font(None, 16)
        self.text_colour = (255, 255, 255)

        self.world = None  # Get this later, after loading


    def render(self):
        """ Actually perform rendering. """

        self.surf.fill(self.BG_COLOR)

        self.surf.blit(*self.world.hero.draw())
        self.surf.blit(*self.world.monster.draw())

        pygame.display.flip()

