from main_char import Hero
from bad_char import Enemy
from good_char import Goodie
from lightning_powerup import Flash
from shroom_powerup import Shroom
import pygame, random, sys, os
from pygame.locals import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)


FPS = 80
PLAYERMOVERATE = 3

DIRECTORY = os.path.dirname(__file__)
HS_FILE = 'highscore.txt'

BADDIERATES = {'one' : {'ADDNEWBADDIERATE1':25,'ADDNEWGOODIERATE1':30}, # until 500
               'two' : {'ADDNEWBADDIERATE2':20,'ADDNEWGOODIERATE2':31}, # above 500
               'three' : {'ADDNEWBADDIERATE3':15,'ADDNEWGOODIERATE3':32}, # above 1500
               'four' : {'ADDNEWBADDIERATE4':13,'ADDNEWGOODIERATE4':37}, # above 3000
               'five' : {'ADDNEWBADDIERATE5':11,'ADDNEWGOODIERATE5':39}, # above 5000
               'six' : {'ADDNEWBADDIERATE6':9,'ADDNEWGOODIERATE6':41}, # above 7000
               'seven' : {'ADDNEWBADDIERATE7':6,'ADDNEWGOODIERATE7':43}, # above 10k
               }


def load_data(DIRECTORY, HS_FILE):
	with open(os.path.join(DIRECTORY, HS_FILE), 'r') as f:
		try:
			highscore = float(f.read())
		except:
			highscore = 0
	return highscore


def initialization():
	pygame.init()
	mainClock = pygame.time.Clock()
	windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
	pygame.display.set_caption('Antisocial')
	pygame.mouse.set_visible(False)

	font = pygame.font.SysFont(None, 35)
	
	hs = load_data(DIRECTORY,HS_FILE)

	highScore = main_menu(windowSurface, font, hs)

	return windowSurface, mainClock, font, highScore


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


def main_menu(windowSurface, font, hs):
	windowSurface.fill(BACKGROUNDCOLOR)
	drawText('∆ Antisocial ∆', font, windowSurface, (WINDOW_WIDTH/3) , (WINDOW_HEIGHT/3))
	drawText(f'HIGH SCORE: {hs}', font, windowSurface, (WINDOW_WIDTH/3) - 50, (WINDOW_HEIGHT/3) + 50)
	pygame.display.update()
	waitForPlayerToPressKey()
	return hs

def moveFigureDown(enemies, reverseCheat, score):
	for e in enemies:
		if not reverseCheat:
			e['rect'].move_ip(0, e['speed'])
		elif reverseCheat:
			e['rect'].move_ip(0, -5)
			score -= 0.3
	return score


def delFigurePastBottom(enemies, resized_h):
    for e in enemies[:]:
        if e['rect'].top > resized_h:
            enemies.remove(e)

def drawFigures(wS, enemies):
	for e in enemies:
			wS.blit(e['surface'], e['rect'])


def addNewGoodiesAndEnemies(enemyAddCounter, goodGuyAddCounter, enemies, good_guys, goodie, enemy, wordNr, wordNr2, resized_w):
	
    if enemyAddCounter >= BADDIERATES[wordNr]['ADDNEWBADDIERATE' + wordNr2]:
        enemyAddCounter = BADDIERATES[wordNr]['ADDNEWBADDIERATE' + wordNr2]
        if enemyAddCounter == BADDIERATES[wordNr]['ADDNEWBADDIERATE' + wordNr2]:
             enemyAddCounter = 0
             newEnemy = enemy.addNewFigure(resized_w)
             enemies.append(newEnemy)
    if goodGuyAddCounter >= BADDIERATES[wordNr]['ADDNEWGOODIERATE' + wordNr2]:
        goodGuyAddCounter = BADDIERATES[wordNr]['ADDNEWGOODIERATE' + wordNr2]
        if goodGuyAddCounter == BADDIERATES[wordNr]['ADDNEWGOODIERATE' + wordNr2]:   
            goodGuyAddCounter = 0
            newGood = goodie.addNewFigure(resized_w)
            good_guys.append(newGood)
    
    return enemyAddCounter, goodGuyAddCounter


def checkScore(enemyAddCounter, goodGuyAddCounter, enemies, good_guys, goodie, enemy, score, resized_w):
	if score > 10000:
		return addNewGoodiesAndEnemies(enemyAddCounter, goodGuyAddCounter, enemies, good_guys, goodie, enemy, 'seven', '7', resized_w)
	elif score > 7000:
		return addNewGoodiesAndEnemies(enemyAddCounter, goodGuyAddCounter, enemies, good_guys, goodie, enemy, 'six', '6', resized_w)
	elif score > 5000:
		return addNewGoodiesAndEnemies(enemyAddCounter, goodGuyAddCounter, enemies, good_guys, goodie, enemy, 'five', '5', resized_w)
	elif score > 3000:	
		return addNewGoodiesAndEnemies(enemyAddCounter, goodGuyAddCounter, enemies, good_guys, goodie, enemy, 'four', '4', resized_w)
	elif score > 1500:
		return addNewGoodiesAndEnemies(enemyAddCounter, goodGuyAddCounter, enemies, good_guys, goodie, enemy, 'three', '3', resized_w)
	elif score > 500:
		return addNewGoodiesAndEnemies(enemyAddCounter, goodGuyAddCounter, enemies, good_guys, goodie, enemy, 'two', '2', resized_w)
	elif score < 500:
		if enemyAddCounter == BADDIERATES['one']['ADDNEWBADDIERATE1']:
			enemyAddCounter = 0
			newEnemy = enemy.addNewFigure(resized_w)
			enemies.append(newEnemy)

		if goodGuyAddCounter == BADDIERATES['one']['ADDNEWGOODIERATE1']:
			goodGuyAddCounter = 0
			newGood = goodie.addNewFigure(resized_w)
			good_guys.append(newGood)

	return enemyAddCounter, goodGuyAddCounter


def game_over(wS, font, score, lastScore, topScore, hs, resized_w, resized_h):

	drawText('GAME OVER', font, wS, (resized_w /3), (resized_h / 3))
	drawText(f'Score: {round(score,2)}', font, wS, (resized_w / 3), (resized_h / 3) + 30)
	drawText('Press a key to play again.', font, wS,
	             (resized_w / 3) - 80, (resized_h / 3) + 100)

	if score > topScore:
		topScore = score

	if score > hs:
		hs = score
		drawText('NEW HIGH SCORE!', font, wS,
				(resized_w / 3) - 40, (resized_h / 3) + 60)
		with open(os.path.join(DIRECTORY, HS_FILE), 'w') as f:
			f.write(str(hs) + '\n')
	lastScore = score
	pygame.display.update()
	waitForPlayerToPressKey()

	return score, lastScore, topScore, hs


def main():
	wS, clock, font, hs = initialization()
	hero = Hero('Stobko')
	enemy = Enemy('badbi4')
	goodie = Goodie('maimen')
	flash = Flash('flashki')
	shroom = Shroom('shroomski')
	
	heroImage = hero.get_image()
	heroRect = hero.get_rectangle()

	lastScore = 0.0
	topScore = 0.0
	resized_w, resized_h = pygame.display.get_surface().get_size()

	while True:
		
		heroRect.topleft = (resized_w / 2, resized_h - 50)

		score = 0.0
		iteration = 0
		enemyAddCounter = 0
		goodGuyAddCounter = 0
		PLAYERMOVERATE = 3

		enemies =[]
		good_guys = []
		flashes = []
		shrooms = []
		
		moveLeft = moveRight = moveUp = moveDown = False
		reverseCheat = False
		
		
		while True:

			score += 1

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.QUIT()
					sys.exit()

				if event.type == VIDEORESIZE:
					wS = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					resized_w, resized_h = pygame.display.get_surface().get_size()

				if event.type == KEYDOWN:
					if event.key == ord('x'):
						reverseCheat = True

					if event.key == K_LEFT or event.key == ord('a'):
						moveRight = False
						moveLeft = True
					if event.key == K_RIGHT or event.key == ord('d'):
						moveLeft = False
						moveRight = True
					if event.key == K_UP or event.key == ord('w'):
						moveDown = False
						moveUp = True
					if event.key == K_DOWN or event.key == ord('s'):
						moveUp = False
						moveDown = True

				if event.type == KEYUP:
					if event.key == ord('x'):
						reverseCheat = False
					if event.key == K_ESCAPE:
						pygame.QUIT()
						sys.exit()
				                           
					if event.key == K_LEFT or event.key == ord('a'):
						moveLeft = False
					if event.key == K_RIGHT or event.key == ord('d'):
						moveRight = False
					if event.key == K_UP or event.key == ord('w'):
						moveUp = False
					if event.key == K_DOWN or event.key == ord('s'):
						moveDown = False	

			if not reverseCheat:
				enemyAddCounter += 1
				goodGuyAddCounter += 1

			enemyAddCounter, goodGuyAddCounter = checkScore(enemyAddCounter, goodGuyAddCounter, enemies, good_guys, goodie, enemy, score, resized_w)
		    
			flashes = flash.addNewFlashToList(iteration, flashes, resized_w, resized_h)

			shrooms = shroom.addNewShroomToList(iteration, shrooms, resized_w, resized_h)


			heroRect = hero.movePlayerAround(moveLeft, moveRight, moveUp, moveDown, heroRect, PLAYERMOVERATE, resized_w, resized_h)

			score = moveFigureDown(enemies, reverseCheat, score)
			score = moveFigureDown(good_guys, reverseCheat, score)

			delFigurePastBottom(enemies, resized_h)
			delFigurePastBottom(good_guys, resized_h)

			wS.fill(BACKGROUNDCOLOR)

			drawText('Score: %s' % (round(score,2)), font, wS, 10, 0)
			drawText('Last: %s' % (round(lastScore, 2)), font, wS, 10, 20)
			drawText('Top: %s' % (round(topScore, 2)), font, wS, 10, 40)
			drawText('Speed: %s' % (PLAYERMOVERATE), font, wS, 10, 60)

			wS.blit(heroImage, heroRect)

			drawFigures(wS, enemies)
			drawFigures(wS, good_guys)
			drawFigures(wS, flashes)
			drawFigures(wS, shrooms)

			pygame.display.update()	

					
			score += hero.checkPlayerHitGoodie(heroRect, good_guys)
			score += shroom.checkForCollisionWithShroom(heroRect, shrooms)

			if flash.checkForCollisionWithFlash(heroRect, flashes):
				if random.randint(0,10) % 2 == 0:
					PLAYERMOVERATE += 1
				else:
					if PLAYERMOVERATE > 1:
						PLAYERMOVERATE -= 1
				heroRect.move_ip(0, PLAYERMOVERATE)

			if enemy.checkForCollision(heroRect, enemies):
				break
			
			iteration += 1
			clock.tick(FPS)

		score,lastScore, topScore, hs = game_over(wS, font, score, lastScore, topScore, hs, resized_w, resized_h)

if __name__ == '__main__':
	main()