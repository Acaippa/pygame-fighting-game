import pygame
from settings import*

class Tile:
	def __init__(self, path, pos):
		self.display_surface = pygame.display.get_surface()
		self.path = path
		self.pos = pos
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(topleft = pos)

	def scale(self, value=ZOOM):
		self.image = pygame.transform.scale(self.image, (self.image.get_width()*ZOOM, self.image.get_height()*ZOOM))
		self.rect = self.image.get_rect(topleft=self.pos)

	def get_size(self):
		return self.image.get_width(), self.image.get_height()

	def draw(self):
		self.display_surface.blit(self.image, self.pos)