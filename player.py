
import pygame
from spriteSheet import spriteSheet
from time import perf_counter


JUMP_SPEED = -18
GRAVITY = 1
ATTACK_DURATION_SEC = 0.2
WALK_FRAME_DURATION_SEC = 0.1
CENTER_CORRECTION_PX = 50
HEALTH = 1
DEATH_FRAME_TIME_SEC = 2

PLAYER_HEIGHT = 96
PLAYER_WIDTH = 48
PLAYER_FRAME_WIDTH = 96

BLACK = (0,0,0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
DARK_BLUE = (0, 0, 100)

class player(pygame.sprite.Sprite):
	def __init__(self, startX, startY):
		self.x = startX
		self.y = startY
		self.sprite_sheet_image = pygame.image.load('frog.png').convert_alpha()
		self.sprite_sheet = spriteSheet(self.sprite_sheet_image)
		self.hitbox = pygame.Rect(startX, startY, 48, 96)
		self.attackHitbox = pygame.Rect(startX + 48, startY + 15,96 - 48,6)
		
		self.walk_frames = []

		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 1, 32, 32, BLACK, 3))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 2, 32, 32, BLACK, 3))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 3, 32, 32, BLACK, 3))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 4, 32, 32, BLACK, 3))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 5, 32, 32, BLACK, 3))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 6, 32, 32, BLACK, 3))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 7, 32, 32, BLACK, 3))

		self.jump_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 6, 32, 32, BLUE, 3)

		self.attack_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 0, 32, 32, BLACK, 3) 
		
		self.crouch_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 8, 32, 32, BLACK, 3) 
		
		self.crouch_attack_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 9, 32, 32, BLACK, 3) 
		
		self.death_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 11, 32, 32, BLACK, 3) 
		
		self.startAttackTime = 0
		self.startWalkTime = 0
		self.currentFrame = 0
		self.isFacingRight = True
		self.inAir = False
		self.isAttacking = False
		self.isCrouching = False
		self.speedX = 1
		self.speedY = 0
		self.altFrame = False
		self.health = HEALTH
		self.isDying = False
		self.isDead = False
		self.loadNextLevel = False
		self.deathTime = 0
		
	def canMoveRight(self, xOffset, floorMaxX, nextFloorY):
		pActX = self.x + xOffset
		if self.isFacingRight:
			pActX -= CENTER_CORRECTION_PX
		if pActX <= floorMaxX - 5:
			return True
		else: 
			if self.y <= nextFloorY:
				return True
			else:
				#print("player y = ", self.y, "y needed = ", nextFloorY, "floor max x = ", floorMaxX)
				#print("player x = ", self.x, "ACTUAL player x = ", pActX)
				#print("")
				return False
				
	def canMoveLeft(self, xOffset, floorMinX, nextFloorY):
		pActX = self.x + xOffset
		if self.isFacingRight:
			pActX -= CENTER_CORRECTION_PX
		if pActX >= floorMinX - 5:
			return True
		else: 
			if self.y <= nextFloorY:
				return True
			else:
				#print("player y = ", self.y, "y needed = ", nextFloorY, "floor max x = ", floorMaxX)
				#print("player x = ", self.x, "ACTUAL player x = ", pActX)
				#print("")
				return False
		
		
	def levelComplete(self):
		if self.loadNextLevel == True:
			self.x = 40
			self.loadNextLevel = False
			return True
		return False
		
	def getDeadStatus(self):
		if self.isDying == True:
			#print("player is dying")
			if perf_counter() - self.deathTime > DEATH_FRAME_TIME_SEC:
				self.isDead = True
				#print("player is dead")
		return self.isDead
		
	def takeDamage(self):
		if self.health > 0: #can't take damage unless health > 0
			self.health -= 1
			if self.health <= 0:
				#print("starting to die")
				self.isDying = True
				self.deathTime = perf_counter()
		
	def getPosX(self):
		return self.x
		
	def setPosX(self, x):
		self.x = x
		
	def getPosY(self):
		return self.y
		
	def getFacingRight(self):
		return self.isFacingRight
		
	def getHitBox(self):
		return self.hitbox
		
	def getAttackHitBox(self):
		return self.attackHitbox
		
	def resetFrame(self):
		self.startWalkTime = 0
		self.currentFrame = 0
		self.isCrouching = False
	
	#return false if player (but not level) moves, true if v.v.
	def moveRight(self, xOffset, levelWidth, screenWidth):
		if self.isDying == False:
			if self.isCrouching: 
				return False
			if self.startWalkTime == 0:
				self.startWalkTime = perf_counter()
			if self.isFacingRight == False:
				self.isFacingRight = True
				self.x += CENTER_CORRECTION_PX
			if xOffset < levelWidth - screenWidth:
				if self.x < (screenWidth / 2) - 48:
					self.x += self.speedX
				else: 
					return True
			else:
				if self.x < screenWidth - 10:
					self.x += self.speedX
				else:
					self.loadNextLevel = True
			self.hitbox = pygame.Rect(self.x, self.y, 48, 96)
		return False
	
	#return false if player (but not level) moves, true if v.v.	
	def moveLeft(self, xOffset, levelWidth, screenWidth):
		if self.isDying == False:
			if self.isCrouching:
				return
			if self.startWalkTime == 0:
				self.startWalkTime = perf_counter()
			if self.isFacingRight == True:
				self.isFacingRight = False
				self.x -= CENTER_CORRECTION_PX
			if xOffset > 0:
				if self.x > (screenWidth / 2) - CENTER_CORRECTION_PX - 48:
					self.x -= self.speedX
				else: 
					return True
			else:
				if self.x > -48:
					self.x -= self.speedX
			self.hitbox = pygame.Rect(self.x + CENTER_CORRECTION_PX, self.y, 48, 96)
		return False
	
	#todo: fix fact that this currently puts players head just beneath the floor
	# need to add player height to floor value when placing player
	def applyGravity(self, floor):
		if self.altFrame == True: #change Y speed every other frame for less 'heavy' feel
			self.speedY += GRAVITY
			self.y += self.speedY
		if self.y > floor:
			self.y = floor
			self.hitbox = pygame.Rect(self.x, self.y, 48, 96)
			self.inAir = False
			self.speedY = 0
		adjustedHitboxX = self.x
		adjustedCrochHitboxX = self.x
		if self.isFacingRight == False:
			adjustedHitboxX += CENTER_CORRECTION_PX
			adjustedCrochHitboxX = adjustedHitboxX - 30
		if self.isCrouching:
			self.hitbox = pygame.Rect(adjustedCrochHitboxX, self.y + 40, 60, 56)
		else:
			self.hitbox = pygame.Rect(adjustedHitboxX, self.y, 48, 96)
			
	def getFrame(self):
		if self.isDying == True:
			return self.death_frame
		elif self.isAttacking == True:
			if self.isCrouching == False:
				return self.attack_frame
			else:
				return self.crouch_attack_frame
		elif self.inAir == True:
			return self.jump_frame
		elif self.isCrouching == True:
			return self.crouch_frame
		else:
			return self.walk_frames[self.currentFrame]
	
	def updateWalkFrame(self):
		if self.isDying == False:
			if self.startWalkTime != 0:
				if((perf_counter() - self.startWalkTime) > WALK_FRAME_DURATION_SEC):
					self.currentFrame += 1
					self.currentFrame %= len(self.walk_frames)
					self.startWalkTime = perf_counter()
				
	def updateAttackFrame(self):
		if self.isAttacking == True:
			if((perf_counter() - self.startAttackTime) > ATTACK_DURATION_SEC):
				self.isAttacking = False
				
	def jump(self):
		if self.isDying == False:
			if self.inAir == False:
				self.speedY += JUMP_SPEED
				self.inAir = True
		
	def attack(self):
		if self.isDying == False and self.isDead == False:
			if self.isAttacking == False:
				self.isAttacking = True
				self.startAttackTime = perf_counter()
				attackX = self.x
				attackY = self.y + 15
				if self.isFacingRight:
					attackX += 48
				if self.isCrouching:
					attackY += 33
				self.attackHitbox = pygame.Rect(attackX, attackY, 96 - 48, 6)
				return True
			else:
				return False
		else:
			return False
		
	def toggleAltFrame(self):
		self.altFrame = not self.altFrame
		
	def crouch(self):
		if self.isDying == False:
			if self.isCrouching == False:
				self.isCrouching = True
		
	def update(self):
		self.applyGravity()
		self.updateWalkFrame()
		self.updateAttackFrame()
		self.toggleAltFrame()
		
	
	