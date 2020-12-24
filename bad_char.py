from entity import Entity
import pygame, random, os

WINDOW_WIDTH = 600

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
	
	def __init__(self, name, health=100):
		Entity.__init__(self,name, health)
		self.image = None
		self.rect = None
		self.size = 0
		self.speed = 0


	def addNewFigure(self, resized_w):
		size = random.randint(ENEMYMINSIZE, ENEMYMAXSIZE)
		
		speed = random.randint(ENEMYMINSPEED, ENEMYMAXSPEED)
		
		newFigure = {'rect' : pygame.Rect(random.randint(0,
                        resized_w - size), 0 - size, size, size),
	        		'speed' : speed,
	        		'surface' : pygame.transform.scale(self.get_image(),(size, size)),
	         }

		return newFigure


	def checkForCollision(self, heroRect, enemies):
		for e in enemies:
			if heroRect.colliderect(e['rect']):
				return True
		return False


	def get_size(self):
		return self.size


	def get_speed(self):
		return self.speed


	def get_image(self):
		self.image = random.choice(enemies_list)
		self.image = pygame.image.load(self.image).convert()
		return self.image


	def get_rectangle(self):
		return self.get_image().get_rect()


	def __str__(self):
		return f'{self.name} with {get_health(self)} health'


	def __repr__(self):
		return self.__str__