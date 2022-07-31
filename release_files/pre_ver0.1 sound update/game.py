import pygame
from tile import*
from player import*
from menues import*

class Game:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.background = pygame.transform.scale(pygame.image.load('images/background/sky.png'), self.display_surface.get_size())

		self.state = "game"

		self.visibleList = []
		self.obsticleList = []
		self.entityList = pygame.sprite.Group()

		self.wonMenu = WonMenu()
		self.lossMenu = LossMenu()
		self.pauseMenu = PauseMenu()

		self.ground = Tile('images/background/ground.png', (2000000, 2000000))
		self.ground.scale()

		for i in range(self.display_surface.get_width() // self.ground.get_size()[0]):
			ground = Tile('images/background/ground.png', (i*self.ground.get_size()[0], self.display_surface.get_height() - self.ground.get_size()[1]))
			ground.scale()
			self.visibleList.append(ground)
			self.obsticleList.append(ground)

		self.player = Player(self.obsticleList)
		self.enemy = Enemy(self.obsticleList, self.entityList, (self.display_surface.get_width() - 300,200))
		self.entityList.add(self.enemy)
		self.entityList.add(self.player)

	def run(self):
		self.display_surface.blit(self.background, (0,0))
		for i in self.visibleList:
			i.draw()

		# Check for a win.
		if self.enemy.dead:
			self.state = "won"
		if self.player.dead:
			self.state = "loss"

		if self.state == "game":
			# Pass the entitylist to the players in order to see if they are hitting them
			self.player.draw(self.entityList)
			self.enemy.draw(self.entityList, True)

			keyboard = pygame.key.get_pressed()
			if keyboard[pygame.K_ESCAPE]:
				self.state = "pause"

		if self.state == "won":
			self.wonMenu.run()
			if self.wonMenu.replayButton.clicked:
				self.__init__()
				self.state = "game"

			if self.wonMenu.quitButton.clicked:
				self.state = "quit"

		if self.state == "loss":
			self.lossMenu.run()
			if self.lossMenu.retryButton.clicked:
				self.__init__()
				self.state == "game"

			if self.lossMenu.quitButton.clicked:
				self.state = "quit"

		if self.state == "pause":
			self.pauseMenu.run()
			if self.pauseMenu.returnButton.clicked:
				self.state = "game"

			if self.pauseMenu.quitButton.clicked:
				self.state = "quit"
