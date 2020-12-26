"""This is the class for the bad characters."""
import random
import os
import pygame
from entity import Entity


ENEMY_DIR = "players/bad/"
enemies_list = []

for dirpath, dirnames, files in os.walk(os.path.abspath(ENEMY_DIR)):
    for file in files:
        if file.endswith('.png'):
            enemies_list.append(ENEMY_DIR + file)

ENEMYMINSIZE = 10
ENEMYMAXSIZE = 30

ENEMYMINSPEED = 1
ENEMYMAXSPEED = 4


class Enemy(Entity):
    """this is the class for the enemies"""
    def __init__(self, name):
        Entity.__init__(self,name)
        self.image = None
        self.rect = None
        self.size = 0
        self.speed = 0


    def add_new_figure(self, resized_w):
        """Add new figure"""
        size = random.randint(ENEMYMINSIZE, ENEMYMAXSIZE)

        speed = random.randint(ENEMYMINSPEED, ENEMYMAXSPEED)

        new_figure = {'rect' : pygame.Rect(random.randint(0,
                        resized_w - size), 0 - size, size, size),
                    'speed' : speed,
                    'surface' : pygame.transform.scale(self.get_image(),(size, size)),
             }

        return new_figure


    def check_for_collision(self, hero_rect, enemies):
        """checking for collisions"""
        for e in enemies:
            if hero_rect.colliderect(e['rect']):
                return True
        return False


    def get_size(self):
        """get the size of the character"""
        return self.size


    def get_speed(self):
        """get the speed of the character"""
        return self.speed


    def get_image(self):
        """get a random image from the list with bad guys"""
        self.image = random.choice(enemies_list)
        self.image = pygame.image.load(self.image).convert()
        return self.image


    def get_rectangle(self):
        """get the corresponding rectangle"""
        return self.get_image().get_rect()


    def __str__(self):
        return f'{self.name}'


    def __repr__(self):
        return self.__str__
