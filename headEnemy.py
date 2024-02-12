
import pygame
from spriteSheet import spriteSheet
from time import perf_counter

REST_TIME_SEC = 3
ATTACK_TIME_SEC = 1
DEATH_FRAME_TIME_SEC = 1
HEALTH = 3

BLACK = (0,0,0)

class headEnemy(pygame.sprite.Sprite):
	def __init__(self, startX, startY):
		self.x = startX
		self.y = startY
		self.sprite_sheet_image = pygame.image.load('headEnemy.png').convert_alpha()
		self.sprite_sheet = spriteSheet(self.sprite_sheet_image)
		self.attackTime = 0
		self.health = HEALTH
		self.isAttacking = False
		self.isDying = False
		self.isDead = False
		self.deathTime = 0
		self.hitbox = pygame.Rect(startX + 50, startY + 44, 43, 50)
		
		self.rest_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 0, 32, 32, BLACK, 3)
		
		self.attack_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 1, 32, 32, BLACK, 3)
		
		self.death_frames = []
		
		self.death_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 2, 32, 32, BLACK, 3))
		self.death_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 3, 32, 32, BLACK, 3))
	
	def takeDamage(self):
		if self.isDying == True:
			return False
		self.health -= 1
		if self.health <= 0:
			self.isDying = True
			self.deathTime = perf_counter()
		return True
	
	def getDeadStatus(self):
		return self.isDead
		
	def getDyingStatus(self):
		return self.isDying
	
	def getHitBox(self):
		return self.hitbox
		
	def getPosX(self):
		return self.x
		
	def getPosY(self):
		return self.y	
		
	def moveX(self, val):
		self.x += val
		self.hitbox = pygame.Rect(self.x + 50, self.y + 44, 43, 50)
		
	def getFrame(self):
		if self.isAttacking == True:
			return self.attack_frame
		elif self.isDying == True:
			if((perf_counter() - self.deathTime) > DEATH_FRAME_TIME_SEC * 2):
				self.isDead = True
				return self.death_frames[1]
			elif((perf_counter() - self.deathTime) > DEATH_FRAME_TIME_SEC):
				return self.death_frames[1]
			else: 
				return self.death_frames[0]
		else:
			return self.rest_frame
			
	def update(self):
		if self.isDying == False:
			if self.isAttacking == True:
				if((perf_counter() - self.attackTime) > ATTACK_TIME_SEC):
					self.isAttacking = False
				return False
			else:
				if((perf_counter() - self.attackTime) > REST_TIME_SEC):
					self.attackTime = perf_counter()
					self.isAttacking = True
					return True
		else:
			self.isAttacking = False
		return False