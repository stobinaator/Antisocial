from entity import Entity
import pygame, random

WINDOW_WIDTH = 600

GOOD_DIR = "players/good/stobko.png"



GOODMINSIZE = 10
GOODMAXSIZE = 30


GOODMINSPEED = 1
GOODMAXSPEED = 4


class Goodie(Entity):
	
	def __init__(self, name, health=100):
		Entity.__init__(self,name, health)
		self.image = pygame.image.load(GOOD_DIR).convert()
		self.rect = self.image.get_rect()
		self.size = 0
		self.speed = 0
		self.points = 0


	def addNewFigure(self):
		size = random.randint(GOODMINSIZE, GOODMAXSIZE)
		
		speed = random.randint(GOODMINSPEED, GOODMAXSPEED)
		
		points = 2 * (50-size)
		newFigure = {'rect' : pygame.Rect(random.randint(0,
                        WINDOW_WIDTH - size), 0 - size, size, size),
	        		'speed' : speed,
	        		'points' : points,
	        		'surface' : pygame.transform.scale(self.get_image(),(size, size)),
	         }

		return newFigure


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