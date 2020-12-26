"""This is the class for the main character."""
import pygame
from entity import Entity


PLAYERS_DIR = "players/player.png"

class Hero(Entity):
    """this is the class for the main character that you play with."""
    def __init__(self, name):
        Entity.__init__(self,name)
        self.image = pygame.image.load(PLAYERS_DIR).convert()
        self.rect = self.image.get_rect()


    def move_player_around(self, move_left, move_right, move_up, move_down,
                         player_rect, PLAYER_MOVE_RATE, resized_w, resized_h):
        """move player around"""
        if move_left:
            player_rect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
            if player_rect.centerx - 10 < 0:
                player_rect.x = resized_w - 10
                player_rect.y = player_rect.y
        if move_right:
            player_rect.move_ip(PLAYER_MOVE_RATE, 0)
            if player_rect.centerx + 10 > resized_w:
                player_rect.x = 10
                player_rect.y = player_rect.y
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0, -1 * PLAYER_MOVE_RATE)
        if move_down and player_rect.bottom < resized_h:
            player_rect.move_ip(0, PLAYER_MOVE_RATE)
        return player_rect


    def check_player_hit_goodie(self, hero_rect, good_guys):
        """check if the player hit any good guys"""
        for g in good_guys[:]:
            if hero_rect.colliderect(g['rect']):
                s = int(g['points'])
                good_guys.remove(g)
                if s is not None:
                    return s
        return 0


    def get_image(self):
        """getting the image"""
        return self.image

    def get_rectangle(self):
        """getting the rectangle"""
        return self.rect

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return self.__str__
