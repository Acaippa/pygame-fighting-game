import pygame
from settings import*

class InfoBar:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.ownSurface = pygame.surface.Surface((20*ZOOM/5,70*ZOOM/5))
		

	def draw(self, pos, health, maxHealth, stamina):
		if health <= 0: # return True if the player is dead
			return True

		self.ownSurface.fill('#333333')

		# healthbar
		self.healthBar = pygame.surface.Surface((15*ZOOM/5,int((65*ZOOM/5)/maxHealth*health)))
		self.healthBar.fill('#ff0000')
		self.ownSurface.blit(self.healthBar, (0,0))

		# staminabar
		self.staminaBar = pygame.surface.Surface(((4*ZOOM/5,int((65*ZOOM/5)/100*stamina))))
		self.staminaBar.fill('#ffffff')
		self.ownSurface.blit(self.staminaBar, (15*ZOOM/5, 0))

		self.display_surface.blit(self.ownSurface, pos)


