import pygame

class MainMenu:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.background = pygame.transform.scale(pygame.image.load('images/menues/main_menu/background.png').convert(), self.display_surface.get_size())

		self.playButton = Button(text="Play", pos=(200,200))
		self.optionsButton = Button(text="Options", pos=(200,400))
		self.quitButton = Button(text="Quit", pos=(200,600))

	def run(self):
		self.display_surface.blit(self.background, (0,0))
		self.playButton.draw()
		self.optionsButton.draw()
		self.quitButton.draw()

class SettingsMenu:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font("fonts/Raleway-ExtraBold.ttf", 70)
		self.background = pygame.transform.scale(pygame.image.load("images/menues/main_menu/background.png").convert(), self.display_surface.get_size())
		self.background.set_alpha(100)

		self.quitButton = Button(text="Quit", pos=(150,900))

	def run(self):
		self.display_surface.blit(self.background, (0,0))
		self.quitButton.draw()

class WonMenu(): # Gets displayed when you kill the enemy.
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.wonText = Text(text="You won!")
		self.replayButton = Button(text="Replay", pos=(200,400))
		self.quitButton = Button(text="Quit to main menu", pos=(200, 600))

	def run(self):
		self.replayButton.draw()
		self.quitButton.draw()
		self.wonText.draw(("center",20))

class LossMenu():
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.lossText = Text(text="You lost!")
		self.retryButton = Button(text="Retry", pos=(200,400))
		self.quitButton = Button(text="Quit to main menu", pos=(200, 600))

	def run(self):
		self.lossText.draw(("center", 20))
		self.retryButton.draw()
		self.quitButton.draw()

class PauseMenu:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.pauseText = Text(text="Paused")
		self.returnButton = Button(text="Return", pos=(200, 400))
		self.quitButton = Button(text="Quit", pos=(200,600))

	def run(self):
		self.pauseText.draw(("center", 20))
		self.returnButton.draw()
		self.quitButton.draw()

class Button:
	def __init__(self, *args, **kwargs):
		self.display_surface = pygame.display.get_surface()
		self.fontSize = kwargs.get('fontSize', 70)
		self.font = pygame.font.Font('fonts/Raleway-ExtraBold.ttf', self.fontSize)
		self.highlightFont = pygame.font.Font('fonts/Raleway-ExtraBold.ttf', self.fontSize)
		self.pos = kwargs.get('pos', (0,0))
		self.text = kwargs.get('text', "")
		self.fontColor = kwargs.get('fontColor', (0,0,0))
		self.command = kwargs.get('command', None)
		self.clicked = False
		self.clickCheck = False
		self.notHolding = False

		self.displayed_font = self.font.render(self.text, True, self.fontColor)
		self.shadow = self.highlightFont.render(self.text, True, (255 - int(self.fontColor[0]), 255 - int(self.fontColor[1]), 255 - int(self.fontColor[2])))
		self.rect = self.displayed_font.get_rect(topleft=self.pos)


	def draw(self):
		self.buttonSurface = pygame.Surface(self.displayed_font.get_size(), pygame.SRCALPHA, 32)
		self.buttonSurface = self.buttonSurface.convert_alpha()
		pos = pygame.mouse.get_pos()
		mouseClicked = pygame.mouse.get_pressed()
		self.clicked = False

		# TODO: Check if the mouse has not been pressed while it has been inside the button

		if self.rect.collidepoint(pos) and mouseClicked[0] and self.clickCheck == False: # Checking for the initial click.
				fontColor = 255 - int(self.fontColor[0]), 255 - int(self.fontColor[1]), 255 - int(self.fontColor[2])
				self.displayed_font = self.font.render(self.text, True, fontColor)
				self.shadow = self.highlightFont.render(self.text, True, (255 - int(fontColor[0]), 255 - int(fontColor[1]), 255 - int(fontColor[2])))
				self.clickCheck = True

		if self.rect.collidepoint(pos) == False and mouseClicked[0] and self.clickCheck == True: # Checking if the user left the button without releasing the click button.
			self.displayed_font = self.font.render(self.text, True, self.fontColor)
			self.shadow = self.highlightFont.render(self.text, True, (255 - int(self.fontColor[0]), 255 - int(self.fontColor[1]), 255 - int(self.fontColor[2])))
			self.clickCheck = False

		if self.rect.collidepoint(pos) and mouseClicked[0] == False and self.clickCheck == True: # Checking if the user released the button while inside the boundries of the button. If so the button is active.
			self.displayed_font = self.font.render(self.text, True, self.fontColor)
			self.shadow = self.highlightFont.render(self.text, True, (255 - int(self.fontColor[0]), 255 - int(self.fontColor[1]), 255 - int(self.fontColor[2])))
			self.clicked = True
			if self.command != None: # Run the command for the button if it exists.
				self.command()
			self.clickCheck = False

	
		if self.rect.collidepoint(pos): # Shadow when mouse hovers over button.
			self.buttonSurface.blit(self.shadow, (2,2))
		self.buttonSurface.blit(self.displayed_font, (0,0))

		self.display_surface.blit(self.buttonSurface, self.pos)


class Text:
	def __init__(self, **kwargs):
		self.display_surface = pygame.display.get_surface()
		# TODO: add a global font setting for the size of the font.
		self.textSize = kwargs.get("size", 70)
		self.font = pygame.font.Font("fonts/Raleway-ExtraBold.ttf", self.textSize)
		self.text = kwargs.get("text", "lorem ipsum")
		self.renderedFont = self.font.render(self.text, True, "#000000")

	def draw(self, pos):
		self.pos = pos
		# Centering on X axis.
		if pos[0] == "center":
			self.pos = self.display_surface.get_width()//2 - self.renderedFont.get_width()//2, pos[1]
		# Centering on Y axis.
		if pos[1] == "center":
			self.pos = pos[0], self.display_surface.get_height()//2

		print(self.pos)
		self.display_surface.blit(self.renderedFont, self.pos)

