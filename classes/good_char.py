"""This is the class for the good character."""
import random
import pygame
import os
from .entity import Entity

DIRECTORY = os.path.abspath(os.getcwd())
GOOD_DIR = DIRECTORY+"/players_images/good/ceci.png"

GOODMINSIZE = 10
GOODMAXSIZE = 30

GOODMINSPEED = 1
GOODMAXSPEED = 4


class Goodie(Entity):
    """class for the good guy that gives you points"""
    def __init__(self, name):
        Entity.__init__(self,name)
        self.image = pygame.image.load(GOOD_DIR).convert()
        self.rect = self.image.get_rect()
        self.size = 0
        self.speed = 0
        self.points = 0


    def add_new_figure(self, resized_w):
        """adding the new figures"""
        size = random.randint(GOODMINSIZE, GOODMAXSIZE)

        speed = random.randint(GOODMINSPEED, GOODMAXSPEED)

        points = 2 * (50-size)
        new_figure = {'rect' : pygame.Rect(random.randint(0,
                        resized_w - size), 0 - size, size, size),
                    'speed' : speed,
                    'points' : points,
                    'surface' : pygame.transform.scale(self.get_image(),(size, size)),
             }

        return new_figure


    def get_size(self):
        """get the size"""
        return self.size

    def get_speed(self):
        """get the speed"""
        return self.speed

    def get_points(self):
        """get the points"""
        return self.points

    def get_image(self):
        """get the image"""
        return self.image

    def get_rectangle(self):
        """get the rect"""
        return self.rect

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return self.__str__
