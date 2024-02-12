

import pygame
from spriteSheet import spriteSheet
from time import perf_counter

VELOCITY = 1
FRAME_TIME_SEC = 0.1
DEATH_FRAME_TIME_SEC = 1
HURT_VELOCITY = -2
HURT_TIME_SEC = 0.5
HEALTH = 4
REST_TIME = 2
JUMP_SPEED = -18
X_SPEED = -10
GRAVITY = 1

BLACK = (0,0,0)

class worm(pygame.sprite.Sprite):
	def __init__(self, startX, startY):
		self.x = startX 
		self.y = startY
		self.sprite_sheet_image = pygame.image.load('worm.png').convert_alpha()
		self.sprite_sheet = spriteSheet(self.sprite_sheet_image)
		self.currentFrame = 0
		self.frameTime = 0
		self.hitbox = pygame.Rect(startX, startY, 60, 96)
		self.isDying = False
		self.isDead = False
		self.isHurt = False
		self.hurtTime = 0
		self.deathTime = 0
		self.health = HEALTH
		self.isFalling = True
		self.restStartTime = 0
		self.isResting = False
		self.isJumping = False
		self.speedY = 0
		self.speedX = 0
		
		self.walk_frames = []

		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 0, 32, 32, BLACK, 5))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 1, 32, 32, BLACK, 5))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 2, 32, 32, BLACK, 5))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 3, 32, 32, BLACK, 5))
		
		self.hurt_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 4, 32, 32, BLACK, 5)
		
		self.death_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 5, 32, 32, BLACK, 5)
	
	def getPosX(self):
		return self.x
		
	def getPosY(self):
		return self.y

	def moveX(self, val):
		self.x += val
		
	def getHitBox(self):
		return self.hitbox
		
	def getDeadStatus(self):
		return self.isDead
		
	def getDyingStatus(self):
		return self.isDying
		
	def takeDamage(self):
		if self.isDying == True:
			return False
		if self.isHurt == True:
			return False# already hurt, give enemy short window of invincibility
		self.health -= 1
		if self.health <= 0:
			self.isHurt = False
			self.isDying = True
			self.deathTime = perf_counter()	
			return True
		else:
			self.isHurt = True
			self.hurtTime = perf_counter()
			return True
		
	def getFrame(self):
		if self.isDying == True:
			if((perf_counter() - self.deathTime) > DEATH_FRAME_TIME_SEC):
				self.isDead = True
			return self.death_frame
		elif self.isHurt == True:
			return self.hurt_frame
		else:
			return self.walk_frames[self.currentFrame]
			
	def jump(self):
		if self.isDying == False:
			if self.isJumping == False:
				self.speedY += JUMP_SPEED
				self.isJumping = True
				
	def update(self, floor):
		if self.isHurt:
			#self.x -= VELOCITY
			if perf_counter() - self.hurtTime > HURT_TIME_SEC:
				self.isHurt = False
		elif self.isDying:
			self.y = self.y
		else:
			if self.isFalling:
				self.y += VELOCITY
				if self.y >= floor - 63:
					self.y = floor - 63
					self.isFalling = False
					self.isResting = True
					self.restStartTime = perf_counter()
			if self.isResting:
				if perf_counter() - self.restStartTime > REST_TIME:
					self.isResting = False
					self.jump()
			if self.isJumping:
				self.speedY += GRAVITY
				self.x += X_SPEED
				self.y += self.speedY
				if self.y >= floor - 63:
					self.y = floor - 63
					self.isJumping = False
					self.isResting = True
					self.restStartTime = perf_counter()				
			self.hitbox = pygame.Rect(self.x, self.y + 6, 60, 96)
			if((perf_counter() - self.frameTime) > FRAME_TIME_SEC):
					self.currentFrame += 1
					self.currentFrame %= len(self.walk_frames)
					self.frameTime = perf_counter()
		if(self.x < -100):
			return False
		return True