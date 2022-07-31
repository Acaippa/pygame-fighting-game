import pygame
import random

class SFX:
	def __init__(self):
		pygame.init()
		self.menu_hover = self.load("hover.wav")
		self.mouse_hold = self.load("hold.wav")
		self.mouse_release = self.load("release.wav")

		self.hurt = self.load("hurt1.wav")
		self.hit_air = self.load("hit_air.wav")


	def load(self, path):
		return pygame.mixer.Sound(f"sounds/{path}")

	def play_menu_hover(self):
		self.menu_hover.set_volume(0.1)
		self.menu_hover.play()

	def play_mouse_hold(self):
		self.mouse_hold.play()

	def play_mouse_release(self):
		self.mouse_release.play()

	def play_hit_air(self):
		self.hit_air.play()

	def play_hurt(self):
		self.hurt.set_volume(0.3)
		self.hurt.play()