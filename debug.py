import pygame

class Debug:
	def __init__(self, text):
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.SysFont('Sans', 30)
		self.renderedFont = self.font.render(str(text), True, ("#000000"))
		self.display_surface.blit(self.renderedFont,(0,0))