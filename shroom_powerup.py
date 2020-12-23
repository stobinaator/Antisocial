from entity import Entity
import pygame, random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

POWERUP_DIR = "players/powerups/red.png"

POWERUPSIZE = 15


class Shroom(Entity):
	
	def __init__(self, name, health=100):
		Entity.__init__(self,name, health)
		self.image = pygame.image.load(POWERUP_DIR).convert_alpha()
		self.rect = self.image.get_rect()
		self.size = 0
		self.speed = 0
		self.points = 200


	def addNewFigure(self):
		size = POWERUPSIZE
		
		newFigure = {'rect' : pygame.Rect(random.randint(0, WINDOW_WIDTH - size), 
                                      random.randint(0, WINDOW_HEIGHT - size), size, size),
	        		'points' : self.points,
	        		'surface' : pygame.transform.scale(self.get_image(),(size, size)),
	         }

		return newFigure

	def checkForCollisionWithShroom(self, heroRect, powerups):
		for p in powerups[:]:
			if heroRect.colliderect(p['rect']):
				s = int(p['points'])
				powerups.remove(p)
				if s != None:
					return s
		return 0

	def addNewShroomToList(self, iteration, powerups):
		if iteration % 600 == 0:
			newShroom = self.addNewFigure()
			powerups.append(newShroom)

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
		return f'{self.name} with {get_health(self)} health'

	def __repr__(self):
		return self.__str__