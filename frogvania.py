
import pygame
import ptext
from time import perf_counter
from spriteSheet import spriteSheet
from player import player
from headEnemy import headEnemy
from fireProjectile import fireProjectile
from eye import eye
from faceOnStick import faceOnStick
from flower import flower
from worm import worm
from tomokoSnake import tomokoSnake
from mobiusCorn import mobiusCorn
from boss import boss


pygame.init()
clock = pygame.time.Clock()
FPS = 180

SCREEN_WIDTH = 1200 #600
SCREEN_HEIGHT = 600 #500

FLOOR = 300 
LEVEL_1_FLOOR = 300
LEVEL_4_FLOOR = 320
LEVEL_6_FLOOR = 330

LEVEL_3_FLOOR_1 = 457
LEVEL_3_FLOOR_2 = 408
LEVEL_3_FLOOR_3 = 308

LEVEL_3_FLOOR_2_X_THRESH = 250
LEVEL_3_FLOOR_3_X_THRESH = 850

LEVEL_WIDTH = 2000

BLACK = (0,0,0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (190, 251, 253)
DARK_BLUE = (0, 0, 100)
LEVEL_4_BG = (5, 99, 129)
LEVEL_5_BG = (17, 66, 82)
LEVEL_6_BG = (38,37,37)
LEVEL_7_BG = (0,0,0)
LEVEL_5_FFG = (14,28,14)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FROG - MAN!")


whipTongue = pygame.mixer.Sound("whipTongue.mp3")
hit = pygame.mixer.Sound("hit.wav")

fosOuch = pygame.mixer.Sound("tomokoFos.wav")#("fosOw.mp3")
headOuch = pygame.mixer.Sound("ethanHead.wav")#("headOuch.wav")
flowOuch = pygame.mixer.Sound("tomokoFlower.wav")#("flowOuch.mp3")
wormOuch = pygame.mixer.Sound("tomokoWorm.wav")#("wormOw.mp3")
eyeOuch = pygame.mixer.Sound("lydianYell.wav")#("tomokoAAAA.wav")
tsOuch = pygame.mixer.Sound("tSnakeOuch.wav")
mcOuch = pygame.mixer.Sound("mcOuch.wav")
finalBossDeath = pygame.mixer.Sound("tomokoAAAAdown.wav")
victorySong = pygame.mixer.Sound("victorySong.wav")

title1 = pygame.image.load("title1.png")
t1Rect = title1.get_rect()
title2 = pygame.image.load("title2.png")
t2Rect = title2.get_rect()
gameOver = pygame.image.load("gameOver.png")
goRect = gameOver.get_rect()
end1 = pygame.image.load("end1.png")
end2 = pygame.image.load("end2.png")
end1Rect = end1.get_rect()
end2Rect = end2.get_rect()

fg = pygame.image.load("testLand.png")
fg_b = pygame.image.load("fg_b.png")
fg_c = pygame.image.load("fg_c.png")
fg_d = pygame.image.load("fg_d.png")
fg_e = pygame.image.load("fg_e.png")
fg_e.set_colorkey(LEVEL_4_BG)
fg_f = pygame.image.load("fg_f.png")
fg_f.set_colorkey(LEVEL_5_BG)
fg_g = pygame.image.load("fg_g.png")
fg_g.set_colorkey(LEVEL_6_BG)
fg_h = pygame.image.load("fg_h.png")
fg_h.set_colorkey(LEVEL_7_BG)

ffg_f = pygame.image.load("ffg_f.png")
ffg_f.set_colorkey(LEVEL_5_FFG)

fgList = []
fgList.append(fg)
fgList.append(fg_b)
fgList.append(fg_c)
fgList.append(fg_d)
fgList.append(fg_e)
fgList.append(fg_f)
fgList.append(fg_g)
fgList.append(fg_h)



bg = pygame.image.load("bg.png")
bg.set_colorkey(LIGHT_BLUE)

bg_b = pygame.image.load("bg_b.png")
bg_b.set_colorkey(LIGHT_BLUE)

bg_e = pygame.image.load("bg_e.png")
bg_e.set_colorkey(LEVEL_4_BG)

bg_f = pygame.image.load("bg_f.png")
bg_f.set_colorkey(LEVEL_5_BG)

bg_g = pygame.image.load("bg_g.png")
bg_g.set_colorkey(LEVEL_6_BG)

bg_h = pygame.image.load("bg_h.png")
bg_h.set_colorkey(LEVEL_7_BG)

bgList = []
bgList.append(bg)
bgList.append(bg_b)
bgList.append(bg)
bgList.append(bg)
bgList.append(bg_e)
bgList.append(bg_f)
bgList.append(bg_g)
bgList.append(bg_h)

bg2 = pygame.image.load("bg2.png")
bg2.set_colorkey(LIGHT_BLUE)

bg2_e = pygame.image.load("bg2_e.png")
bg2_e.set_colorkey(LEVEL_4_BG)

bg2_f = pygame.image.load("bg2_f.png")
bg2_f.set_colorkey(LEVEL_5_BG)

bg2_g = pygame.image.load("bg2_g.png")
bg2_g.set_colorkey(LEVEL_6_BG)

bg2_h = pygame.image.load("bg2_h.png")
bg2_h.set_colorkey(LEVEL_7_BG)

bg2List = []
bg2List.append(bg2)
bg2List.append(bg2)
bg2List.append(bg2)
bg2List.append(bg2)
bg2List.append(bg2_e)
bg2List.append(bg2_f)
bg2List.append(bg2_g)
bg2List.append(bg2_h)

numTexts = 8
orig_text = []
iterators = []
texts = []

text_orig_1 = """GENERIC MAD SCIENTIST TYPE CHARACTER: 'Well well well.  You've finally managed """
text_orig_2 = """to track me down.  But it's too late. Soon, you'll have no memory of ever having"""
text_orig_3 = """been human.  And once I drink this potion, I'm going to smash you!  And THEN, I'm""" 
text_orig_4 = """going to disperse my formula into the air so that EVERYONE will be frogs!  HAAAAH!!!"""
text_orig_5 = """HAAA HA HA HA HA HA HA HA HA HA HAH!! HA HAHHHHA HAAAHAAA. Hee Hee HEEEEHA."""
text_orig_6 = """MMMMWWWWHAAA hahahahEhEHEHEHHHAHAHAHA!! MWHHA HAAAHAAA. HAR HAR HAR HAR HAR!"""
text_orig_7 = """hahahahHAHAHAHAHAHAHAHAhhahahhehehehhahahehehehEEEHEHEEHEEHHAAAAA! ......ha."""
text_orig_8 = """                                 ......heh.'"""

text_iterator_1 = iter(text_orig_1)
text_iterator_2 = iter(text_orig_2)
text_iterator_3 = iter(text_orig_3)
text_iterator_4 = iter(text_orig_4)
text_iterator_5 = iter(text_orig_5)
text_iterator_6 = iter(text_orig_6)
text_iterator_7 = iter(text_orig_7)
text_iterator_8 = iter(text_orig_8)

text1 = ''
text2 = ''
text3 = ''
text4 = ''
text5 = ''
text6 = ''
text7 = ''
text8 = ''

orig_text.append(text_orig_1)
orig_text.append(text_orig_2)
orig_text.append(text_orig_3)
orig_text.append(text_orig_4)
orig_text.append(text_orig_5)
orig_text.append(text_orig_6)
orig_text.append(text_orig_7)
orig_text.append(text_orig_8)

iterators.append(text_iterator_1)
iterators.append(text_iterator_2)
iterators.append(text_iterator_3)
iterators.append(text_iterator_4)
iterators.append(text_iterator_5)
iterators.append(text_iterator_6)
iterators.append(text_iterator_7)
iterators.append(text_iterator_8)

texts.append(text1)
texts.append(text2)
texts.append(text3)
texts.append(text4)
texts.append(text5)
texts.append(text6)
texts.append(text7)
texts.append(text8)

gameOpen = True
textLoop = True #only show text one time
gameWon = False

def getFloorMaxX(level, curFloorY):
	if level == 3:
		if curFloorY == LEVEL_3_FLOOR_3: 
			return 2400 #TODO FIX: for now just means 'beyond level end'
		elif curFloorY == LEVEL_3_FLOOR_2:
			return LEVEL_3_FLOOR_3_X_THRESH
		else:
			return LEVEL_3_FLOOR_2_X_THRESH
			
def getYForNextFloor(curFloorY):
	if curFloorY == LEVEL_3_FLOOR_1:
		return LEVEL_3_FLOOR_2
	if curFloorY == LEVEL_3_FLOOR_2:
		return LEVEL_3_FLOOR_3
	if curFloorY == LEVEL_3_FLOOR_3:
		return LEVEL_3_FLOOR_3
		
def setNewCaption(level):
	if level == 1:
		pygame.display.set_caption("FROG - MAN! LEVEL : 2")
	if level == 2:
		pygame.display.set_caption("FROG - MAN! LEVEL : 3")
	if level == 3:
		pygame.display.set_caption("FROG - MAN! LEVEL : 4")
	if level == 4:
		pygame.display.set_caption("FROG - MAN! LEVEL : 5")
	if level == 5:
		pygame.display.set_caption("FROG - MAN! LEVEL : 6")
	if level == 6:
		pygame.display.set_caption("FROG - MAN! LEVEL : 7")
	if level == 7:
		pygame.display.set_caption("FROG - MAN! LEVEL : 8")
			
	
level = 0#7
while gameOpen == True:
	p = player(50, 200)
	floor = FLOOR

	hList = []
	eyeList = []
	fosList = []
	flowerList = []
	fpList = []
	wormList = []	
	tSnakeList = []	
	mcList = []	
	bossList = []

	mainGameLoop = True
	bossLoop = False
	panLoop = True

	levelWidth = LEVEL_WIDTH
	screenWidth = SCREEN_WIDTH
	xOffset = 0

	screen.blit(title1, t1Rect)
	pygame.display.update()

	pygame.mixer.music.load("Recording.wav")#("frogOpen.wav")
	pygame.mixer.music.play(-1)

	waiting = True
	while waiting is True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					waiting = False
			if event.type == pygame.QUIT:
				quit = True
				mainGameLoop = False
				waiting = False
				gameOpen = False
				break
				
	if gameOpen == False:
		break
				
	screen.blit(title2, t2Rect)
	pygame.display.update()
	pygame.mixer.music.stop()

	waiting = True
	while waiting is True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					waiting = False
			if event.type == pygame.QUIT:
				quit = True
				mainGameLoop = False
				waiting = False
				gameOpen = False
				break
				
	if gameOpen == False:
		break
				
	pygame.mixer.music.load("test.wav")
	pygame.mixer.music.play(-1)
	
	#debug enemies
	#fosList.clear()
	#eyeList.clear()
	#flowerList.clear()
	
	
	pygame.display.set_caption("FROG - MAN! LEVEL : 1")
	
	MS_frames = [] #blank array for mad scientist 'sprite' images
	MS_sprite_sheet_image = pygame.image.load('madScientist.png').convert_alpha()
	MS_sprite_sheet = spriteSheet(MS_sprite_sheet_image)
	for i in range(9): #num MS sprites
		MS_frames.append(MS_sprite_sheet.getImage(MS_sprite_sheet_image, i, 32, 32, BLACK, 3))
	MS_frames.append(MS_sprite_sheet.getImage(MS_sprite_sheet_image, 9, 32, 32, BLACK, 4))
	MS_frames.append(MS_sprite_sheet.getImage(MS_sprite_sheet_image, 10, 32, 32, BLACK, 4))
	MS_frames.append(MS_sprite_sheet.getImage(MS_sprite_sheet_image, 11, 32, 32, BLACK, 5))
	MS_frames.append(MS_sprite_sheet.getImage(MS_sprite_sheet_image, 12, 32, 32, BLACK, 5))
	
	just_started = True
	gameWon = False

	while mainGameLoop:
	

		if p.levelComplete() == True or just_started == True:
			
			if(just_started == False):
				level += 1
			just_started = False
			setNewCaption(level) #pygame.display.set_caption("FROG - MAN! LEVEL : ", str(level))
			xOffset = 0
			if(level == 0):				
				i = eye(1600, 270)
				eyeList.append(i)
				fos = faceOnStick(3000, 270)
				fosList.append(fos)
				flw = flower(1800, 265)#265
				flowerList.append(flw)
			if(level == 1):
				fpList.clear()
				flowerList.clear()
				fos = faceOnStick(300, 270)
				fosList.append(fos)
				i = eye(1600, 270)
				eyeList.append(i)
				i2 = eye(1700, 270)
				eyeList.append(i2)
				i3 = eye(1800, 270)
				eyeList.append(i3)
				h = headEnemy(1800, 299)
				hList.append(h)
			if(level == 2):
				fpList.clear()
				hList.clear()
				w = worm(1300, -100)
				w2 = worm(1900, -100)
				wormList.append(w)
				wormList.append(w2)
			if(level == 3):
				wormList.clear()
				hList.clear()
				flowerList.clear()
				flw2a = flower(LEVEL_3_FLOOR_2_X_THRESH + 30, LEVEL_3_FLOOR_2 - 30)
				flowerList.append(flw2a)
				hd2 = headEnemy(LEVEL_3_FLOOR_3_X_THRESH + 30, LEVEL_3_FLOOR_3)
				hList.append(hd2)
				flw2b = flower(1800, 270)
				flowerList.append(flw2b)
			if(level == 4):
				hList.clear()
				flowerList.clear()
				fpList.clear()
				ts1 = tomokoSnake(-1000, LEVEL_4_FLOOR - 35)
				tSnakeList.append(ts1)
			if(level == 5):
				tSnakeList.clear()
				mc1 = mobiusCorn(-1200, LEVEL_4_FLOOR - 100)
				mcList.append(mc1)
			if(level == 6):
				mcList.clear()
				pygame.mixer.music.stop()
				pygame.mixer.music.load("crickets.wav")
				pygame.mixer.music.play(-1)
			if(level == 7):
				pygame.mixer.music.stop()
				pygame.mixer.music.load("frogOpen.wav")
				pygame.mixer.music.play(-1)
				
		
		# 3, at x >= 329, floor = 430 
		# 3, at x >= 920, floor = 330
		oldFloor = floor
		if level == 2: 
			if p.getPosX() > 100:
				floor = 480
		elif level == 3:
			pActX = p.getPosX() + xOffset			
			isFR = p.getFacingRight()
			if isFR:
				pActX -= 50
			if pActX > LEVEL_3_FLOOR_2_X_THRESH and pActX < LEVEL_3_FLOOR_3_X_THRESH:
				floor = LEVEL_3_FLOOR_2
			elif pActX >= LEVEL_3_FLOOR_3_X_THRESH: 
				floor = LEVEL_3_FLOOR_3
			else:
				floor = LEVEL_3_FLOOR_1
		elif level == 4:
			floor = LEVEL_4_FLOOR
		elif level == 5:
			floor = LEVEL_4_FLOOR
		elif level == 6:
			floor = LEVEL_6_FLOOR
		elif level == 7: #330, 480
			if p.getPosX() > 100:
				floor = 480
			pActX = p.getPosX() + xOffset	
			if pActX > 900:
				mainGameLoop = False
				bossLoop = True
				pygame.mixer.music.stop()
				pygame.mixer.music.load("boss.wav")
				pygame.mixer.music.play(0)
		else:
			floor = FLOOR
				
		if oldFloor != floor:
			#print("floor is now = ", floor)
			#print("pX is = ", p.getPosX())
			#print("xOffset is = ", xOffset)
			oldFloor = floor
			
			
				

		if(level <= 3):
			screen.fill(LIGHT_BLUE)
		if(level == 4):
			screen.fill(LEVEL_4_BG)
		if(level == 5):
			screen.fill(LEVEL_5_BG)
		if(level == 6):
			screen.fill(LEVEL_6_BG)
		if(level == 7):
			screen.fill(LEVEL_7_BG)
		if level < 5:
			screen.blit(bg2List[level], (-xOffset / 4, 100))#150
			screen.blit(bgList[level], (-xOffset / 2, 130))#150
		elif level == 5:
			screen.blit(bg2List[level], (-xOffset / 4, 0))#150
			screen.blit(bgList[level], (-xOffset / 2, 0))#150
		elif level == 6:
			screen.blit(bg2List[level], (0, 0))#150
			screen.blit(bgList[level], (-xOffset / 2, 0))#150	
		elif level == 7:
			screen.blit(bg2List[level], (-xOffset / 4, 0))#150
			screen.blit(bgList[level], (-xOffset / 2, 0))#150	
		if(level < 4):
			screen.blit(fgList[level], (-xOffset, 393))
		else:
			screen.blit(fgList[level], (-xOffset, 0))
			
		if level == 5:
			screen.blit(ffg_f, (-xOffset * 2, 400))
		
		keys = pygame.key.get_pressed()  
		if keys[pygame.K_RIGHT]:
			floorY = floor
			if level == 3:
				floorMaxX = getFloorMaxX(level, floor) 
				floorY = getYForNextFloor(floor)
			elif level == 7:
				floorMaxX = 1880
				floorY = 10
			else:
				floorMaxX = 2400
			if p.canMoveRight(xOffset, floorMaxX, floorY): 
				if p.moveRight(xOffset, levelWidth, screenWidth) == True:
					xOffset +=  1
					for h in hList:
						h.moveX(-1)
					for f in flowerList:
						f.moveX(-1)
					for i in eyeList:
						i.moveX(-1)
					for fos in fosList:
						fos.moveX(-1)
					for w in wormList:
						w.moveX(-1)
					for fp in fpList:
						fp.moveX(-1)
					for ts in tSnakeList:
						ts.moveX(-1)
					for mc in mcList:
						mc.moveX(-1)
				
		elif keys[pygame.K_LEFT]:
			if p.moveLeft(xOffset, levelWidth, screenWidth) == True:
				xOffset -=  1
				for h in hList:
					h.moveX(1)
				for f in flowerList:
					f.moveX(1)
				for i in eyeList:
					i.moveX(1)
				for fos in fosList:
					fos.moveX(1)
				for w in wormList:
					w.moveX(1)
				for fp in fpList:
					fp.moveX(1)
				for ts in tSnakeList:
					ts.moveX(1)
				for mc in mcList:
					mc.moveX(1)
			
		elif keys[pygame.K_DOWN]:
			p.crouch()
			
		else:
			p.resetFrame()
		
		p.applyGravity(floor)
		
		for h in hList:
			if abs(h.getPosX() - xOffset) < SCREEN_WIDTH:
				screen.blit(h.getFrame(), (h.getPosX(), h.getPosY()))
				#pygame.draw.rect(screen, (255, 0, 0), h.getHitBox(), 2)  # 2 is the width of the outline
				if h.update() == True:
					fire = fireProjectile(h.getPosX(), h.getPosY())
					fpList.append(fire)
				if h.getDeadStatus() == True:
					hList.remove(h)
				
		for f in flowerList:
			if abs(f.getPosX() - xOffset) < SCREEN_WIDTH:
				screen.blit(f.getFrame(), (f.getPosX(), f.getPosY()))
				#pygame.draw.rect(screen, (255, 0, 0), f.getHitBox(), 2)  # 2 is the width of the outline
				if f.update() == True:
					fire = fireProjectile(f.getPosX(), f.getPosY() - 48)
					fpList.append(fire)
				if f.getDeadStatus() == True:
					flowerList.remove(f)
				
		for i in eyeList:
			screen.blit(i.getFrame(), (i.getPosX(), i.getPosY()))
			#pygame.draw.rect(screen, (255, 0, 0), i.getHitBox(), 2)  # 2 is the width of the outline
			i.update()
			eyeHitBox = i.getHitBox()
			if i.getDyingStatus() == False and eyeHitBox.colliderect(p.getHitBox()):
				p.takeDamage()
			if i.getDeadStatus() == True:
				eyeList.remove(i)
				
		for fos in fosList:
			screen.blit(fos.getFrame(), (fos.getPosX(), fos.getPosY()))
			#pygame.draw.rect(screen, (255, 0, 0), fos.getHitBox(), 2)  # 2 is the width of the outline
			fos.update()
			fosHitBox = fos.getHitBox()
			if fos.getDyingStatus() == False and fosHitBox.colliderect(p.getHitBox()):
				p.takeDamage()
			if fos.getDeadStatus() == True:
				fosList.remove(fos)
				
		for ts in tSnakeList:
			screen.blit(ts.getFrame(), (ts.getPosX(), ts.getPosY()))
			#pygame.draw.rect(screen, (255, 0, 0), ts.getHitBox(), 2)  # 2 is the width of the outline
			ts.update()
			tsHitBox = ts.getHitBox()
			if ts.getDyingStatus() == False and tsHitBox.colliderect(p.getHitBox()):
				p.takeDamage()
			if ts.getDeadStatus() == True:
				tSnakeList.remove(ts)
				
		for mc in mcList:
			screen.blit(mc.getFrame(), (mc.getPosX(), mc.getPosY()))
			#pygame.draw.rect(screen, (255, 0, 0), ts.getHitBox(), 2)  # 2 is the width of the outline
			mc.update()
			mcHitBox = mc.getHitBox()
			if mc.getDyingStatus() == False and mcHitBox.colliderect(p.getHitBox()):
				p.takeDamage()
			if mc.getDeadStatus() == True:
				mcList.remove(mc)
				
		for w in wormList:
			screen.blit(w.getFrame(), (w.getPosX(), w.getPosY()))
			#pygame.draw.rect(screen, (255, 0, 0), w.getHitBox(), 2)  # 2 is the width of the outline
			w.update(480)
			wormHitBox = w.getHitBox()
			if w.getDyingStatus() == False and wormHitBox.colliderect(p.getHitBox()):
				p.takeDamage()
			if w.getDeadStatus() == True:
				wormList.remove(w)		
				
		for fp in fpList:
			fpExists = fp.update()
			screen.blit(fp.getFrame(), (fp.getPosX(), fp.getPosY()))
			fpHitBox = fp.getHitBox()
			#pygame.draw.rect(screen, (255, 0, 0), p.getHitBox(), 2)  # 2 is the width of the outline
			#pygame.draw.rect(screen, (255, 0, 0), fp.getHitBox(), 2)  # 2 is the width of the outline
			if fpHitBox.colliderect(p.getHitBox()):
				p.takeDamage()
			if fpExists == False:
				fpList.remove(fp)
		
		if p.getFacingRight() == True:
			screen.blit(p.getFrame(), (p.getPosX(), p.getPosY()))
		else:
			screen.blit(pygame.transform.flip(p.getFrame(), True, False), (p.getPosX(), p.getPosY()))

		#pygame.draw.rect(screen, (255, 0, 0), p.getHitBox(), 2)  # 2 is the width of the outline
		p.updateWalkFrame()
		p.updateAttackFrame()
		#pygame.draw.rect(screen, (255, 0, 0), p.getAttackHitBox(), 2)  # 2 is the width of the outline

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainGameLoop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP: 
					p.jump()
					#print("player x = ", p.getPosX(), "offset = ", xOffset)
				if event.key == pygame.K_SPACE: 
					canAttack = p.attack()
					if canAttack == True:
						whipTongue.play()
						for h in hList:
							if p.getAttackHitBox().colliderect(h.getHitBox()):
								alive = h.takeDamage()
								hit.play()
								if h.getDyingStatus() == True and alive:
									headOuch.play()
						for e in eyeList:
							if p.getAttackHitBox().colliderect(e.getHitBox()):
								alive = e.takeDamage()
								hit.play()	
								if e.getDyingStatus() == True and alive:
									eyeOuch.play()
						for f in flowerList:
							if p.getAttackHitBox().colliderect(f.getHitBox()):
								alive = f.takeDamage()
								hit.play()
								if f.getDyingStatus() == True and alive == True:
									flowOuch.play()
						for fos in fosList:
							if p.getAttackHitBox().colliderect(fos.getHitBox()):
								alive = fos.takeDamage()
								hit.play()
								if fos.getDyingStatus() == True and alive == True:
									fosOuch.play()
						for ts in tSnakeList:
							if p.getAttackHitBox().colliderect(ts.getHitBox()):
								alive = ts.takeDamage()
								hit.play()
								if ts.getDyingStatus() == True and alive == True:
									tsOuch.play()
						for mc in mcList:
							if p.getAttackHitBox().colliderect(mc.getHitBox()):
								alive = mc.takeDamage()
								hit.play()
								if mc.getDyingStatus() == True and alive == True:
									mcOuch.play()
						for w in wormList:
							if p.getAttackHitBox().colliderect(w.getHitBox()):
								alive = w.takeDamage()
								hit.play()
								if w.getDyingStatus() == True and alive == True:
									wormOuch.play()
					
					
		p.toggleAltFrame()
		#p.update()
		if p.getDeadStatus() == True:
			mainGameLoop = False
				
		pygame.display.update()
		
		clock.tick(FPS)
		
		skipWait = False#True
		
	while bossLoop == True:
	
		#setNewCaption(level) #debug only
		
		screen.fill(LEVEL_7_BG)
		screen.blit(bg2List[level], (-xOffset / 4, 0))#150
		screen.blit(bgList[level], (-xOffset / 2, 0))#150	
		screen.blit(fgList[level], (-xOffset, 0))
		
		MS_abs_pos_X = 1800
		MS_abs_pos_y = 465
		MSframe = 1
		
		while panLoop == True:
		#TODO start music
			screen.fill(LEVEL_7_BG)
			screen.blit(bg2List[level], (-xOffset / 4, 0))#150
			screen.blit(bgList[level], (-xOffset / 2, 0))#150	
			screen.blit(fgList[level], (-xOffset, 0))
			if MSframe <= 8:
				screen.blit(MS_frames[MSframe], (MS_abs_pos_X - xOffset, MS_abs_pos_y))
			elif MSframe <= 10:
				screen.blit(MS_frames[MSframe], (MS_abs_pos_X - xOffset - 32, MS_abs_pos_y - 32))
			elif MSframe <= 12:
				screen.blit(MS_frames[MSframe], (MS_abs_pos_X - xOffset - 64, MS_abs_pos_y - 64))
			
			if xOffset < 800:
				xOffset += 1
				p.setPosX(p.getPosX() - 1)
				screen.blit(p.getFrame(), (p.getPosX(), p.getPosY()))
				#print("new xOffset = ", xOffset) 			
			else: #TODO, make this a nested loop where:
			#1. MS text blits
			#2. music stops
			#3. MS drinks potion (add glug sound)
			#4. MS transitions
			#5. boss music starts
				textLine = 1 #will ++ to numTexts
				while textLoop == True:
					for t in range(textLine):
						if len(texts[t]) < len(orig_text[t]) - 1:
							texts[t] += next(iterators[t])
						elif len(texts[t]) < len(orig_text[t]):
							texts[t] += next(iterators[t])
							textLine += 1
							if textLine == numTexts + 1:
								if skipWait == False:
									pygame.time.delay(14000)
								pygame.mixer.music.stop()
								pygame.mixer.music.load("glug.mp3")
								textLoop = False
						myfont = pygame.font.SysFont('Arial', 30)
						textsurface = myfont.render(texts[t], True, (255, 255, 255))
						screen.blit(textsurface,(100,100 + (30 * t)))
						screen.blit(p.getFrame(), (p.getPosX(), p.getPosY()))
						pygame.display.update()
						
				#screen.blit(p.getFrame(), (p.getPosX(), p.getPosY()))
				if(MSframe > 7):
					pygame.time.delay(500)
				else:
					pygame.time.delay(1000)
				MSframe += 1
				if MSframe == 3:
					pygame.mixer.music.play(9)
				if MSframe == 13:
					#clock.tick(1)
					panLoop = False
					b1 = boss(850, 255)
					bossList.append(b1)
					pygame.mixer.music.stop()
					pygame.mixer.music.load("bossFight.wav")
					pygame.mixer.music.play(-1)
					
			screen.blit(p.getFrame(), (p.getPosX(), p.getPosY()))	
			pygame.display.update()
			#keys = pygame.key.get_pressed()  
			#if keys[pygame.K_SPACE]:
			#	panLoop = False
			
		pygame.draw.rect(screen, (75, 75, 75), (20, 360, 20, 200))
		pygame.draw.rect(screen, (85, 85, 85), (20, 350, 10, 220))
		pygame.draw.rect(screen, (95, 95, 95), (10, 340, 10, 240))
		
		for b in bossList:
			if b.getFacingRight() == False:
				screen.blit(b.getFrame(), (b.getPosX(), b.getPosY()))
			else:
				screen.blit(pygame.transform.flip(b.getFrame(), True, False), (b.getPosX(), b.getPosY()))
			#pygame.draw.rect(screen, (255, 0, 0), ts.getHitBox(), 2)  # 2 is the width of the outline
			b.update(255, p.getPosX())
			bCurrentHitBoxes = b.getHitBoxes() #this will be an ARRAY of hitboxes
			for hBox in bCurrentHitBoxes:
				#pygame.draw.rect(screen, (255, 0, 0), hBox, 2)  # 2 is the width of the outline
				if b.getDyingStatus() == False and hBox.colliderect(p.getHitBox()):
					p.takeDamage()
					break  #don't take multiple hits if colliding with multiple hitboxes
			if b.getDeadStatus() == True:
				bossList.remove(b)
				bossLoop = False
				gameWon = True
			
		if p.getFacingRight() == True:
			screen.blit(p.getFrame(), (p.getPosX(), p.getPosY()))
		else:
			screen.blit(pygame.transform.flip(p.getFrame(), True, False), (p.getPosX(), p.getPosY()))	
				
		keys = pygame.key.get_pressed()  
		if keys[pygame.K_RIGHT]:
			floorMaxX = 1880
			floorY = 10
			if p.canMoveRight(xOffset, floorMaxX, floorY): 
				p.moveRight(xOffset, levelWidth, screenWidth)
				
		elif keys[pygame.K_LEFT]:
			floorMinX = 800 #actual X position (level x)
			floorY = 10
			if p.canMoveLeft(xOffset, floorMinX, floorY): 
				p.moveLeft(0, levelWidth, screenWidth)
			
		elif keys[pygame.K_DOWN]:
			p.crouch()
			
		else:
			p.resetFrame()
		
		p.applyGravity(floor)
		
		p.updateWalkFrame()
		p.updateAttackFrame()		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				bossLoop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP: 
					p.jump()
					#print("player x = ", p.getPosX(), "offset = ", xOffset)
				if event.key == pygame.K_SPACE: 
					canAttack = p.attack()
					if canAttack == True:
						whipTongue.play()	
						for b in bossList:
							bossHitboxes = b.getHitBoxes()
							for hBox in bossHitboxes:
								if p.getAttackHitBox().colliderect(hBox):
									alive = b.takeDamage()
									hit.play()
									if b.getDyingStatus() == True and alive == True:
										finalBossDeath.play()
									break #don't register multiple hits if colliding with more than one hitbox
					
		p.toggleAltFrame()
		if p.getDeadStatus() == True:
			bossLoop = False
			gameWon = False
			#print("you are dead")
			
		pygame.display.update()
		
		clock.tick(FPS)
			
		
	
	if gameWon == True:
		pygame.time.delay(3000)
		screen.blit(end1, end1Rect)
		pygame.display.update()	

		pygame.mixer.music.stop()
		pygame.mixer.music.load("victorySong.wav")#("gameOver.wav")
		pygame.mixer.music.play(0)
		pygame.time.delay(15000)
		screen.blit(end2, end2Rect)
		pygame.display.update()	
		pygame.time.delay(5000)
		secs = 0
		level = 0
		skip = False
	else:
		screen.blit(gameOver, goRect)
		pygame.display.update()	

		pygame.mixer.music.stop()
		pygame.mixer.music.load("end.wav")#("gameOver.wav")
		pygame.mixer.music.play(0)
		secs = 0
		#if(level != 7):
			#level = 0
		#else:
		skip = False
	while secs < 10 and skip == False and gameOpen == True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					skip = True
		if event.type == pygame.QUIT:
				gameOpen = False
				break
		clock.tick(1)
		secs += 1
	
pygame.quit()