from entity import Entity
import pygame

PLAYERS_DIR = "players/player.png"

class Hero(Entity):
	
	def __init__(self, name):
		Entity.__init__(self,name)
		self.image = pygame.image.load(PLAYERS_DIR).convert()
		self.rect = self.image.get_rect()


	def movePlayerAround(self, moveLeft, moveRight, moveUp, moveDown, playerRect, PLAYERMOVERATE, resized_w, resized_h):
	    # move the player around
	    if moveLeft:
	            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
	            if playerRect.centerx - 10 < 0:
	                playerRect.x = resized_w - 10
	                playerRect.y = playerRect.y
	    if moveRight:
	            playerRect.move_ip(PLAYERMOVERATE, 0)
	            if playerRect.centerx + 10 > resized_w:
	                playerRect.x = 10
	                playerRect.y = playerRect.y
	    if moveUp and playerRect.top > 0:
	            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
	    if moveDown and playerRect.bottom < resized_h:
	            playerRect.move_ip(0, PLAYERMOVERATE)
	    return playerRect


	def checkPlayerHitGoodie(self, heroRect, good_guys):
		for g in good_guys[:]:
			if heroRect.colliderect(g['rect']):
				s = int(g['points'])
				good_guys.remove(g)
				if s != None:
					return s	
		return 0
			

	def get_image(self):
		return self.image

	def get_rectangle(self):
		return self.rect

	def __str__(self):
		return f'{self.name}'

	def __repr__(self):
		return self.__str__