"""This is the class for the shroom powerup."""
import random
import pygame
import os
from .entity import Entity

DIRECTORY = os.path.abspath(os.getcwd())
POWERUP_DIR = DIRECTORY+"/players_images/powerups/red.png"

POWERUPSIZE = 15


class Shroom(Entity):
    """the class for the shroom powerup"""
    def __init__(self, name):
        Entity.__init__(self,name)
        self.image = pygame.image.load(POWERUP_DIR).convert_alpha()
        self.rect = self.image.get_rect()
        self.size = 0
        self.speed = 0
        self.points = 200


    def add_new_figure(self, resized_w, resized_h):
        """adding new figures"""
        size = POWERUPSIZE

        new_figure = {'rect' : pygame.Rect(random.randint(0, resized_w - size),
                                      random.randint(0, resized_h - size), size, size),
                    'points' : self.points,
                    'surface' : pygame.transform.scale(self.get_image(),(size, size)),
             }

        return new_figure

    def check_for_collision_with_shroom(self, hero_rect, powerups):
        """checking for collisions"""
        for p in powerups[:]:
            if hero_rect.colliderect(p['rect']):
                s = int(p['points'])
                powerups.remove(p)
                if s is not None:
                    return s
        return 0

    def add_new_shroom_to_list(self, iteration, powerups, resized_w, resized_h):
        """adding new shrooms after X iterations"""
        if iteration % 600 == 0:
            new_shroom = self.add_new_figure(resized_w, resized_h)
            powerups.append(new_shroom)

        return powerups

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
        """get the rectangle"""
        return self.rect

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return self.__str__
