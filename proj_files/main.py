import pygame
from menues import*
from game import*
from List import*

class Main:
	def __init__(self):
		self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
		pygame.font.init()
		pygame.mixer.init()
		self.menuList = List()

		self.gameState = 'mainMenu'
		self.running = True
		self.clock = pygame.time.Clock()
		self.start()


	def start(self): # Initing all the menu objects.
		self.mainMenu = MainMenu()
		self.menuList.append("mainMenu", self.mainMenu)
		self.optionsMenu = SettingsMenu()
		self.menuList.append("optionsMenu", self.optionsMenu)
		self.game = Game()
		self.menuList.append("mainGame", self.game)

	def mainMenuRun(self): # Running the main menu and adding functions for all it's buttons.
		self.mainMenu.run()
		if self.mainMenu.playButton.clicked:
			self.gameState = 'mainGame'  

		if self.mainMenu.optionsButton.clicked:
			self.gameState = "settingsMenu"    

		if self.mainMenu.quitButton.clicked:
			self.running = False

	def optionsMenuRun(self): # Options menu.
		self.optionsMenu.run()

		if self.optionsMenu.quitButton.clicked:
					self.gameState = "mainMenu"

	def mainGameRun(self): # Main game.
		self.game.run()
		if self.game.state == 'quit':
			self.__init__()
			self.gameState = 'mainMenu'

	def run(self): # Handing all the different game states.
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
			self.screen.fill('#000000')
			if self.gameState == 'mainMenu':
				self.mainMenuRun()

			if self.gameState == "settingsMenu":
				self.optionsMenuRun()

			if self.gameState == 'mainGame':
				self.mainGameRun()

			self.clock.tick(60)
			pygame.display.flip()
		quit()

if __name__ == "__main__":
	main = Main()
	main.run()

# fixed zooming bug
# if you sprint and stop you will slide for some time