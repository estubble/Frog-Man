
import pygame
from spriteSheet import spriteSheet
from time import perf_counter

VELOCITY = -2
FRAME_TIME_SEC = 0.3
ORIGIN_X_OFFSET = -5

BLACK = (0,0,0)

class fireProjectile(pygame.sprite.Sprite):
	def __init__(self, startX, startY):
		self.x = startX + ORIGIN_X_OFFSET
		self.y = startY
		self.sprite_sheet_image = pygame.image.load('fireProjectile.png').convert_alpha()
		self.sprite_sheet = spriteSheet(self.sprite_sheet_image)
		self.currentFrame = 0
		self.frameTime = 0
		self.hitbox = pygame.Rect(startX + 30, startY + 57, 33, 36)
		
		self.frames = []

		self.frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 0, 32, 32, BLACK, 3))
		self.frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 1, 32, 32, BLACK, 3))
		self.frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 2, 32, 32, BLACK, 3))
		self.frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 3, 32, 32, BLACK, 3))
	
	def getPosX(self):
		return self.x
		
	def getPosY(self):
		return self.y

	def moveX(self, val):
		self.x += val
		
	def getHitBox(self):
		return self.hitbox
		
	def getFrame(self):
		return self.frames[self.currentFrame]
			
	def update(self):
		self.x += VELOCITY
		self.hitbox = pygame.Rect(self.x + 30, self.y + 57, 33, 36)
		if((perf_counter() - self.frameTime) > FRAME_TIME_SEC):
				self.currentFrame += 1
				self.currentFrame %= len(self.frames)
				self.frameTime = perf_counter()
		if(self.x < -100):
			return False
		return True