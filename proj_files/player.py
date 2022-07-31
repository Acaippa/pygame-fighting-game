import pygame
import os
from settings import*
from healthbar import*
import math
import random
from sounds import*

from debug import*

class Player(pygame.sprite.Sprite):
	def __init__(self, obsticles, pos=(200,200)):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		self.actionList = []

		tempList = []
		for i in range(7): # attack
			image = pygame.image.load(os.getcwd() + f'\\images\\players\\molberg\\attack\\w{i}.png').convert_alpha()
			image = pygame.transform.scale(image, (image.get_width()*ZOOM, image.get_height()*ZOOM))
			tempList.append(image)
		self.actionList.append(tempList)

		tempList = []
		for i in range(9): # idle 
			image = pygame.image.load(os.getcwd() + f'\\images\\players\\molberg\\idle\\i{i}.png').convert_alpha()
			image = pygame.transform.scale(image, (image.get_width()*ZOOM, image.get_height()*ZOOM))
			tempList.append(image)
		self.actionList.append(tempList)

		tempList = []
		for i in range(4): # walking
			image = pygame.image.load(os.getcwd() + f'\\images\\players\\molberg\\walking\\w{i}.png').convert_alpha()
			image = pygame.transform.scale(image, (image.get_width()*ZOOM, image.get_height()*ZOOM))
			tempList.append(image)
		self.actionList.append(tempList)

		self.actionIndex = 1
		self.frameIndex = 0
		self.animationDelay = 0
		self.dead = False
		self.health = 100
		self.force = 10
		self.direction = pygame.math.Vector2()
		self.pos = pos
		self.speed = 5
		self.walking = False
		self.sprintSpeed = 3.5
		self.walkingSpeed = 0.2
		self.maxSpeed = 0
		self.stamina = 100
		self.maxStamina = 100
		self.staminaDecay = 1
		self.staminaRegen = 1
		self.jumpStaminaDecay = 30
		self.gravity = 0.5
		self.falling = True
		self.rect = self.actionList[self.actionIndex][self.frameIndex].get_rect(topleft=self.pos) # Get the rect from the current image using the frame and action index.
		self.obsticlelist = obsticles
		self.jumping = False
		self.jumpVel = 7
		self.attack = False # Indicates if the attack animation should play.
		self.keepAttack = False
		self.attacking = False # Used by enemies to check if the player is attacking.
		self.mask = pygame.mask.from_surface(self.actionList[self.actionIndex][self.frameIndex])
		self.image = self.actionList[self.actionIndex][self.frameIndex]
		self.deltatick = pygame.time.get_ticks()
		self.deltatime = 1
		self.flipped = False
		self.shake = False
		self.shakeCounter = 0
		self.punchTick = 0
		self.attackSpeed = 300 # The amount of milliseconds between a punch
		self.enemy = None
		self.animationDelayIndex = 0

		self.sound = SFX()

		self.InfoBar = InfoBar()

	def walk_right(self):
		keyInput = pygame.key.get_pressed()
		self.actionIndex = 2
		self.maxSpeed += self.walkingSpeed

	def sprint_right(self):
		self.maxSpeed = self.sprintSpeed
		self.stamina -= self.staminaDecay

	def walk_left(self):
		keyInput = pygame.key.get_pressed()
		self.actionIndex = 2
		self.maxSpeed += self.walkingSpeed * -1
	
	def sprint_left(self):
		self.maxSpeed = self.sprintSpeed * -1
		self.stamina -= self.staminaDecay

	def attack_action(self):
		if self.attacking and pygame.sprite.collide_mask(self, self.enemy) and self.shake != True:
			self.enemy.hurt(self.force, self.pos[0])
			self.attacking = False


	def initiateAttack(self):
		if (pygame.time.get_ticks() - self.punchTick) > self.attackSpeed:
			self.punchTick = pygame.time.get_ticks()
			self.sound.play_hit_air()
			self.actionIndex = 0 # Set the action index to attack.
			self.attacking = True # Change this here so we don't loop it. It needs to be reset after the entity has hit the enemy.


	def turn_action(self, bool):
		self.flipped = bool

	def input(self):
		keyInput = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()
		self.actionIndex = 1

		# Jumping.
		if keyInput[pygame.K_SPACE] and self.jumping == False and self.stamina >= self.jumpStaminaDecay:
			if self.stamina - self.jumpStaminaDecay <= 0:
				self.stamina = 0
			else: # Remove stamina.
				self.stamina -= self.jumpStaminaDecay
			self.jumping = True
			self.falling = True

		if self.jumping: # move the entity by less and less upwards
			self.direction.y = self.jumpVel * -1
			self.jumpVel -= 0.5

			if self.jumpVel < -6: # stop jumping
				self.jumpVel = 6
				self.jumping = False

		# Walking.
		if keyInput[pygame.K_d]:
			self.walk_right()
			if keyInput[pygame.K_LSHIFT] and self.stamina > self.staminaDecay:
				self.sprint_right()
			
		if keyInput[pygame.K_a]:
			self.walk_left()

			if keyInput[pygame.K_LSHIFT] and self.stamina > self.staminaDecay:
				self.sprint_left()

		if mouse[0] and self.keepAttack == False:
			self.initiateAttack()

	def update(self):
		try:
			self.customLoop()# Function for other entities so they can have separate own loops for AI and such.
		except Exception as e:
			# print(e)
			pass

		for i in self.obsticlelist: # checking if the player should fall or not
			if self.rect.colliderect(i.rect) and self.falling == True:
				self.falling = False
				self.pos = self.pos[0], i.rect.top - self.rect.height

		# apply friction
		if self.maxSpeed != 0:
			self.maxSpeed *= 0.88

		# apply the speed to the player
		self.direction.x = self.maxSpeed

		# check if the entity is falling or not, if so apply gravity to it
		if self.falling:
			self.direction.y += self.gravity

		# stop falling if the falling is false
		elif self.falling == False:
			self.direction.y = 0

		# regeneration 
		if self.direction.x != 0 and self.stamina < self.maxStamina:
			self.stamina += self.staminaRegen / 2

		# regenerate faster if you stand still
		if self.direction.x == 0 and self.stamina < self.maxStamina:
			self.stamina += self.staminaRegen * 3

		# animation
		if self.actionIndex == 0: # attack
			self.animationDelay = 1
			self.keepAttack = True

		if self.keepAttack:
			self.actionIndex = 0

		if self.actionIndex == 1: # idle
			self.animationDelay = 8

		if self.actionIndex == 2: # walking
			self.animationDelay = 6

		# Check if the frameIndex is larger than the length of the current actionIndex, if it is we increment the frameIndex ONLY if the animationDelayIndex is larger than the designated actions animationDelay. Effectively using the animationDelay as a frame buffer before the next animation frame increment. 
		if self.frameIndex < len(self.actionList[self.actionIndex]) - 1:
			if self.animationDelayIndex >= self.animationDelay:
				self.frameIndex += 1
				self.animationDelayIndex = 0
			else:
				self.animationDelayIndex += 1 # Increment the delayIndex rather than increment the frameIndex.
		else:
			# Put the actionIndex back to idle, and set the attacking variable to false so the entity doesn't keep dealing damage after the animation is done.
			self.frameIndex = 0
			self.actionIndex = 1
			self.keepAttack = False
			self.attacking = False

		# Check if the entity is outside the bounds.
		self.bounds = 0, self.display_surface.get_width()

		# Checking the right side.
		# Divide the length of the rect to check farther out from the screen.
		if self.pos[0] >= self.bounds[1] - (self.rect.width // 2):
			self.pos = self.bounds[1] - (self.rect.width  // 2), self.pos[1]

		# Left side.
		if self.pos[0] <= self.bounds[0] - (self.rect.width // 2):
			self.pos = self.bounds[0] - (self.rect.width  // 2), self.pos[1]

		# Check the position of the enemy and flip the player if it's on rhe right side.
		for i in self.entityList:
			if i != self:
				if i.pos[0] >= self.pos[0]:
					self.turn_action(False)
				else:
					self.turn_action(True)

		self.attack_action()

	def get_delta(self):
		self.deltatime = (pygame.time.get_ticks() - self.deltatick) / 20
		self.deltatick = pygame.time.get_ticks()
		# To prevent the deltatime from rising to ungodly values while we wait in the main menu, we have to set a max value for the deltatime.
		if self.deltatime >= 10:
			self.deltatime = 1

	def draw(self, entitylist, enemy=False, idle=False):
		self.entityList = entitylist # a list of all the enemies in the game

		for i in self.entityList:
			if i != self:
				self.enemy = i

		# uncomment to see the mask outlines at the top of the screen
		# olist = self.mask.outline()
		# pygame.draw.polygon(self.display_surface,(200,150,150),olist,0)

		self.image = self.actionList[self.actionIndex][self.frameIndex]
		self.pos = self.pos[0] + self.direction.x * self.speed * self.deltatime, self.pos[1] + self.direction.y * self.speed * self.deltatime
		self.rect = self.image.get_rect(topleft=self.pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.dead = self.InfoBar.draw(self.pos, self.health, 100, self.stamina) # check if this is true to see if the player is dead
		self.get_delta() # Update the Delta Time

		# make the entity move in a random degree every frame 
		if self.shake: 
			self.shake_pos = self.pos[0] + math.cos(math.radians(random.randint(0,360))) * 10 * (ZOOM/10), self.pos[1] + math.cos(math.radians(random.randint(0,360))) * 10 * (ZOOM/10)	
			if self.shakeCounter < 10:
				self.shakeCounter += 1
			else:
				self.shakeCounter = 0
				self.shake = False

		# flip the entity image, and update the mask
		if self.flipped: 
			self.image = pygame.transform.flip(self.image, True, False)
			self.mask = pygame.mask.from_surface(self.image)


		if not self.shake:
			self.display_surface.blit(self.image, self.pos)
		else:
			self.display_surface.blit(self.image, self.shake_pos)
				
		self.input()
		self.update()

	def hurt(self, amount, position):
		self.shake = True
		self.health -= amount
		if position >= self.pos[0]:
			self.maxSpeed = -5
		else:
			self.maxSpeed = 5

		self.sound.play_hurt()

class Enemy(Player):
	def __init__(self, obsticles, entityList, pos):
		super().__init__(obsticles, pos)
		self.counter = 0
		self.entityList = entityList
		self.distanceToPlayer = 0
		self.attack_distance = 140

	def nothing(self):
		pass

	def input(self):
		# Get the player
		for i in self.entityList:
			if i != self:
				self.player = i

		# Move towards the player.
		dist = (i.pos[0] - self.pos[0])
		if dist > 0:
			self.distanceToPlayer = dist
		else:
			self.distanceToPlayer = dist*-1

		# Check how close the player is to the enemy
		if self.distanceToPlayer < self.attack_distance:
			random.choice([self.initiateAttack, self.nothing, self.nothing])()
		else:
			if self.pos[0] >= self.player.pos[0]:
				random.choice([self.walk_left, self.nothing, self.nothing])()
			else:
				self.walk_right()

		self.attack_distance = random.randint(120, 200)

