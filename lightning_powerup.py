from entity import Entity
import pygame, random

POWERUP_DIR = "players/powerups/flash.png"

POWERUPSIZE = 20

class Flash(Entity):
	
	def __init__(self, name):
		Entity.__init__(self,name)
		self.image = pygame.image.load(POWERUP_DIR).convert_alpha()
		self.rect = self.image.get_rect()
		self.size = 0
		self.speed = 0
		self.points = 0


	def addNewFigure(self, resized_w, resized_h):
		size = POWERUPSIZE
		
		newFigure = {'rect' : pygame.Rect(random.randint(0, resized_w - size), 
                                      random.randint(0, resized_h - size), size, size),
	        		'surface' : pygame.transform.scale(self.get_image(),(size, size)),
	         }

		return newFigure

	def checkForCollisionWithFlash(self, heroRect, powerups):
		for p in powerups[:]:
			if heroRect.colliderect(p['rect']):
				powerups.remove(p)
				return True
		return False

	def addNewFlashToList(self, iteration, powerups, resized_w, resized_h):
		if iteration % 500 == 0:
			newSpeed = self.addNewFigure(resized_w, resized_h)
			powerups.append(newSpeed)

		return powerups

	def get_size(self):
		return self.size

	def get_speed(self):
		return self.speed

	def get_points(self):
		return self.points

	def get_image(self):
		return self.image

	def get_rectangle(self):
		return self.rect

	def __str__(self):
		return f'{self.name}'

	def __repr__(self):
		return self.__str__