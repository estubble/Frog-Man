

import pygame
from spriteSheet import spriteSheet
from time import perf_counter

VELOCITY = 1
FRAME_TIME_SEC = 0.1
DEATH_FRAME_TIME_SEC = 1
HURT_VELOCITY = -2
HURT_TIME_SEC = 0.5
HEALTH = 10#10
REST_TIME = 2
WALK_FRAME_TIME = 0.3
JUMP_SPEED = -30
X_SPEED = -14
GRAVITY = 1
THRESH_HIT = 50
THRESH_WALK = 200
TARGET_X_RIGHT = 850
TARGET_X_LEFT = 50
MAX_SECS_WITHOUT_ATTACK = 10

BLACK = (0,0,0)

#boss states
STATE_STATIONARY = 0
STATE_JUMPING = 1
STATE_WALK = 2
STATE_HIT = 3

class boss(pygame.sprite.Sprite):
	def __init__(self, startX, startY):
		self.x = startX 
		self.y = startY
		self.sprite_sheet_image = pygame.image.load('boss.png').convert_alpha()
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
		self.hitStartTime = 0
		self.walkStartTime = 0
		self.speedY = 0
		self.speedX = 0
		self.state = STATE_STATIONARY
		self.isFacingRight = False
		self.currentSmashFrame = 0
		self.currentWalkFrame = 0
		self.xSpeedPercent = 0
		self.lastPlayerNearTime = perf_counter()
		self.lastState = STATE_STATIONARY
		
		self.walk_frames = [] #walking/spitting fire
		self.smash_frames = [] #hand smash_frames
		self.death_frames = []
		self.hitboxes = [] #need array of hitboxes, how many???
		
		self.break_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 0, 128, 128, BLACK, 3)#standing, between attacks
		
		self.smash_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 1, 128, 128, BLACK, 3))
		self.smash_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 2, 128, 128, BLACK, 3))

		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 3, 128, 128, BLACK, 3))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 4, 128, 128, BLACK, 3))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 5, 128, 128, BLACK, 3))
		self.walk_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 6, 128, 128, BLACK, 3))
		
		self.jump_frame = self.sprite_sheet.getImage(self.sprite_sheet_image, 7, 128, 128, BLACK, 3)
		
		self.death_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 8, 128, 128, BLACK, 3))
		self.death_frames.append(self.sprite_sheet.getImage(self.sprite_sheet_image, 9, 128, 128, BLACK, 3))
		
		self.hitboxes.append(pygame.Rect(startX, startY + 96, 43, 50))
	
	def getFacingRight(self):
		return self.isFacingRight
		
	def getPosX(self):
		return self.x
		
	def getPosY(self):
		return self.y

	def moveX(self, val):
		self.x += val
		
	def getHitBoxes(self): #boss has ARRAY of hitboxes, which change depending on frame
		return self.hitboxes
		
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
		#print("boss health = " + str(self.health))
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
			if((perf_counter() - self.deathTime) > DEATH_FRAME_TIME_SEC * 2):
				self.isDead = True
				return self.death_frames[1]
			elif((perf_counter() - self.deathTime) > DEATH_FRAME_TIME_SEC):
				return self.death_frames[1]
			else: 
				return self.death_frames[0]
		#elif self.isHurt == True:
		#	return self.hurt_frame
		else:
			if self.state == STATE_STATIONARY:
				return self.break_frame#self.walk_frames[self.currentFrame]
			if self.state == STATE_JUMPING:
				return self.jump_frame#self.walk_frames[self.currentFrame]
			if self.state == STATE_HIT:
				return self.smash_frames[self.currentSmashFrame]
			if self.state == STATE_WALK:
				return self.walk_frames[self.currentWalkFrame]
			
	def jump(self):
		if self.isDying == False:
			if self.state != STATE_JUMPING:
				self.speedY += JUMP_SPEED
				self.state = STATE_JUMPING
				if self.isFacingRight:
					distance = abs(self.x - TARGET_X_RIGHT)
					maxDistance = abs(TARGET_X_LEFT - TARGET_X_RIGHT)
					self.xSpeedPercent = distance/maxDistance
				else:
					distance = abs(self.x - TARGET_X_LEFT)
					maxDistance = abs(TARGET_X_LEFT - TARGET_X_RIGHT)
					self.xSpeedPercent = distance/maxDistance
					
	def updateHitboxes(self): #need state, frame in state, and X and Y
		self.hitboxes.clear()
		if self.isFacingRight:
			if self.state == STATE_STATIONARY:
				self.hitboxes.append(pygame.Rect(self.x + 255, self.y + 180, 80, 20))
				self.hitboxes.append(pygame.Rect(self.x + 70, self.y + 360, 160, 20))
			elif self.state == STATE_WALK:
				self.hitboxes.append(pygame.Rect(self.x + 255, self.y + 180, 80, 20))
				self.hitboxes.append(pygame.Rect(self.x + 70, self.y + 360, 160, 20))
			elif self.state == STATE_JUMPING:
				self.hitboxes.append(pygame.Rect(self.x, self.y + 96, 80, 20))
				self.hitboxes.append(pygame.Rect(self.x + 70, self.y + 360, 80, 20))
			elif self.state == STATE_HIT:
				if self.currentSmashFrame == 0:
					#self.hitboxes.append(pygame.Rect(self.x + 200, self.y + 96, 80, 20))
					self.hitboxes.append(pygame.Rect(self.x + 70, self.y + 360, 160, 20))
				else:
					self.hitboxes.append(pygame.Rect(self.x + 295, self.y + 340, 80, 40))
					self.hitboxes.append(pygame.Rect(self.x + 200, self.y + 320, 80, 20))
					self.hitboxes.append(pygame.Rect(self.x + 70, self.y + 360, 160, 20))
		else:
			if self.state == STATE_STATIONARY:
				self.hitboxes.append(pygame.Rect(self.x + 25, self.y + 180, 80, 20))
				self.hitboxes.append(pygame.Rect(self.x + 150, self.y + 360, 160, 20))
			elif self.state == STATE_WALK:
				self.hitboxes.append(pygame.Rect(self.x + 25, self.y + 180, 80, 20))
				self.hitboxes.append(pygame.Rect(self.x + 150, self.y + 360, 160, 20))
			elif self.state == STATE_JUMPING:
				self.hitboxes.append(pygame.Rect(self.x, self.y + 96, 80, 20))
				self.hitboxes.append(pygame.Rect(self.x + 150, self.y + 360, 160, 20))
			elif self.state == STATE_HIT:
				if self.currentSmashFrame == 0:
					#self.hitboxes.append(pygame.Rect(self.x, self.y + 360, 80, 20))
					self.hitboxes.append(pygame.Rect(self.x + 150, self.y + 360, 160, 20))
				else:
					self.hitboxes.append(pygame.Rect(self.x, self.y + 340, 80, 40))
					self.hitboxes.append(pygame.Rect(self.x + 75, self.y + 280, 80, 20))
					self.hitboxes.append(pygame.Rect(self.x + 150, self.y + 360, 160, 20))
				
	def update(self, floor, playerPosX):
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
					self.lastState = self.state
					self.state = STATE_STATIONARY
					self.restStartTime = perf_counter()
			if self.state == STATE_STATIONARY:
				if perf_counter() - self.restStartTime > REST_TIME:
					fudgedPlayerPosX = playerPosX
					threshHitX = THRESH_HIT
					threshWalkX = THRESH_WALK
					if self.isFacingRight == True:
						fudgedPlayerPosX = playerPosX - 200
						threshHitX = 100
						threshWalkX = 200
					if abs(self.x - fudgedPlayerPosX) < threshHitX and self.lastState != STATE_HIT: #second condition avoids constant missing hits
						self.lastState = self.state
						self.state = STATE_HIT
						self.hitStartTime = perf_counter()
						self.lastPlayerNearTime = perf_counter()
					elif abs(self.x - fudgedPlayerPosX) < threshWalkX or (abs(perf_counter() - self.lastPlayerNearTime) > MAX_SECS_WITHOUT_ATTACK):
						self.lastState = self.state
						self.state = STATE_WALK
						self.walkStartTime = perf_counter()	
						if abs(self.x - fudgedPlayerPosX) <threshWalkX: #if still out of range, keep walking
							self.lastPlayerNearTime = perf_counter()						
					else:
						self.jump()
						self.state = STATE_JUMPING
			if self.state == STATE_JUMPING: 
				self.speedY += GRAVITY
				if self.isFacingRight == True:
					self.x += -X_SPEED * self.xSpeedPercent
				else:
					self.x += X_SPEED * self.xSpeedPercent
				self.y += self.speedY
				if self.y >= floor - 63:
					self.y = floor - 63
					self.lastState = self.state
					self.state = STATE_STATIONARY
					self.restStartTime = perf_counter()
			if self.state == STATE_HIT:
				if perf_counter() - self.hitStartTime > REST_TIME:
					self.currentSmashFrame += 1
					if self.currentSmashFrame >= len(self.smash_frames):
						self.last_state = self.state
						self.state = STATE_STATIONARY
						self.currentSmashFrame = 0
					else: 
						self.hitStartTime = perf_counter()
			if self.state == STATE_WALK:
				if perf_counter() - self.walkStartTime > WALK_FRAME_TIME:
					self.currentWalkFrame += 1
					if self.currentWalkFrame >= len(self.walk_frames):
						self.lastState = self.state
						self.state = STATE_STATIONARY
						self.currentWalkFrame = 0
					else: 
						if self.isFacingRight:
							self.x += 20
						else:
							self.x -= 20
						self.walkStartTime = perf_counter()
			
			#self.hitbox = pygame.Rect(self.x, self.y + 6, 60, 96)
			#if((perf_counter() - self.frameTime) > FRAME_TIME_SEC):
			#		self.currentFrame += 1
			#		self.currentFrame %= len(self.walk_frames)
			#		self.frameTime = perf_counter()
			if self.state != STATE_JUMPING:
				if self.x >= (playerPosX - 100):
					self.isFacingRight = False
				else:
					self.isFacingRight = True
			self.updateHitboxes()
		if(self.x < -100):
			return False
		return True