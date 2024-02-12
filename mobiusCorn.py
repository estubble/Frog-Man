



import pygame
import random
from spriteSheet import spriteSheet
from time import perf_counter

VELOCITY = 1
MAX_VEL = 2
FRAME_TIME_SEC = 0.1
DEATH_FRAME_TIME_SEC = 1
HURT_VELOCITY = 2
HURT_TIME_SEC = 0.5
HEALTH = 5
SCALE_FACTOR = 3
SIZE = 192

BLACK = (0,0,0)

class mobiusCorn(pygame.sprite.Sprite):
	def __init__(self, startX, startY):
		self.x = startX 
		self.y = startY
		self.sprite_sheet_image = pygame.image.load('mobiusCorn.png').convert_alpha()
		self.sprite_sheet = spriteSheet(self.sprite_sheet_image)
		self.currentFrame = 0
		self.frameTime = 0
		self.hitbox = pygame.Rect(startX, startY, SIZE, SIZE)
		self.isDying = False
		self.isDead = False
		self.isHurt = False
		self.hurtTime = 0
		self.deathTime = 0
		self.health = HEALTH
		
		self.walk_frames = []

		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 0, 64, 64, BLACK, SCALE_FACTOR))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 1, 64, 64, BLACK, SCALE_FACTOR))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 2, 64, 64, BLACK, SCALE_FACTOR))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 3, 64, 64, BLACK, SCALE_FACTOR))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 4, 64, 64, BLACK, SCALE_FACTOR))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 5, 64, 64, BLACK, SCALE_FACTOR))
		
		self.hurt_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 6, 64, 64, BLACK, SCALE_FACTOR)
		
		self.death_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 7, 64, 64, BLACK, SCALE_FACTOR)
	
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
			
			
	def update(self):
		if self.isHurt:
			self.x -= VELOCITY
			self.hitbox = pygame.Rect(self.x, self.y, SIZE, SIZE)
			if perf_counter() - self.hurtTime > HURT_TIME_SEC:
				self.isHurt = False
		elif self.isDying:
			self.x = self.x
		else:
			accel = bool(random.getrandbits(1))
			self.x += VELOCITY 
			self.x += accel
			self.hitbox = pygame.Rect(self.x, self.y, SIZE, SIZE)
			if((perf_counter() - self.frameTime) > FRAME_TIME_SEC):
					self.currentFrame += 1
					self.currentFrame %= len(self.walk_frames)
					self.frameTime = perf_counter()
		if(self.x > 3000):
			return False
		return True