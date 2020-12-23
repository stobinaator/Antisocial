
class Entity:

	def __init__(self, name, health):
		self.name = name
		self.health = health


	def get_health(self):
		return int(self.health)

