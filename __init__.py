"""this is the main class where the game loop lives"""
import random
import sys
import os
import pygame
from pygame.locals import *
from classes.main_char import Hero
from classes.bad_char import Enemy
from classes.good_char import Goodie
from classes.lightning_powerup import Flash
from classes.shroom_powerup import Shroom 


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)


FPS = 80
PLAYER_MOVE_RATE = 3

DIRECTORY = os.path.abspath(os.getcwd())
HS_FILE = DIRECTORY+'/highscore.txt'

BADDIERATES = {
'one' : {'ADDNEWBADDIERATE1':25,'ADDNEWGOODIERATE1':30}, # until 500
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
    """initializing some stuff before starting the game"""
    pygame.init()
    main_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                     pygame.RESIZABLE)
    pygame.display.set_caption('Antisocial')
    pygame.mouse.set_visible(False)

    font = pygame.font.SysFont(None, 35)

    hs = load_data(DIRECTORY,HS_FILE)

    high_score = main_menu(screen, font, hs)

    return screen, main_clock, font, high_score


def wait_for_player_to_press_key():
    """just waiting for the player to press escape"""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


def draw_text(text, font, surface, x, y):
    """helper method for drawing text"""
    text_obj = font.render(text, 1, TEXTCOLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x,y)
    surface.blit(text_obj, text_rect)


def main_menu(screen, font, hs):
    """showing this menu before the game"""
    screen.fill(BACKGROUNDCOLOR)
    draw_text('∆ Antisocial ∆', font, screen,
                (WINDOW_WIDTH/3) , (WINDOW_HEIGHT/3))
    draw_text(f'HIGH SCORE: {hs}', font, screen,
                (WINDOW_WIDTH/3) - 50, (WINDOW_HEIGHT/3) + 50)
    pygame.display.update()
    wait_for_player_to_press_key()
    return hs

def move_figure_down(enemies, reverse_cheat, score):
    """mathod for moving the figures automatically down"""
    for e in enemies:
        if not reverse_cheat:
            e['rect'].move_ip(0, e['speed'])
        elif reverse_cheat:
            e['rect'].move_ip(0, -5)
            score -= 0.3
    return score


def del_figure_past_bottom(enemies, resized_h):
    """deleting the figures that have already passed the bottom"""
    for e in enemies[:]:
        if e['rect'].top > resized_h:
            enemies.remove(e)

def draw_figures(screen, enemies):
    """drawing figures every iteration"""
    for e in enemies:
        screen.blit(e['surface'], e['rect'])


def add_new_goodies_and_enemies(enemy_add_counter, good_guy_add_counter,
            enemies, good_guys, goodie, enemy, wordNr, wordNr2, resized_w):


    if enemy_add_counter >= BADDIERATES[wordNr]['ADDNEWBADDIERATE' + wordNr2]:
        enemy_add_counter = BADDIERATES[wordNr]['ADDNEWBADDIERATE' + wordNr2]
        if enemy_add_counter == BADDIERATES[wordNr]['ADDNEWBADDIERATE' + wordNr2]:
            enemy_add_counter = 0
            new_enemy = enemy.add_new_figure(resized_w)
            enemies.append(new_enemy)
    if good_guy_add_counter >= BADDIERATES[wordNr]['ADDNEWGOODIERATE' + wordNr2]:
        good_guy_add_counter = BADDIERATES[wordNr]['ADDNEWGOODIERATE' + wordNr2]
        if good_guy_add_counter == BADDIERATES[wordNr]['ADDNEWGOODIERATE' + wordNr2]:
            good_guy_add_counter = 0
            new_good = goodie.add_new_figure(resized_w)
            good_guys.append(new_good)

    return enemy_add_counter, good_guy_add_counter


def check_score(enemy_add_counter, good_guy_add_counter, enemies, good_guys,
             goodie, enemy, score, resized_w):

    if score > 10000:
        return add_new_goodies_and_enemies(enemy_add_counter, good_guy_add_counter, enemies, good_guys, goodie, enemy, 'seven', '7', resized_w)
    elif score > 7000:
        return add_new_goodies_and_enemies(enemy_add_counter, good_guy_add_counter, enemies, good_guys, goodie, enemy, 'six', '6', resized_w)
    elif score > 5000:
        return add_new_goodies_and_enemies(enemy_add_counter, good_guy_add_counter, enemies, good_guys, goodie, enemy, 'five', '5', resized_w)
    elif score > 3000:
        return add_new_goodies_and_enemies(enemy_add_counter, good_guy_add_counter, enemies, good_guys, goodie, enemy, 'four', '4', resized_w)
    elif score > 1500:
        return add_new_goodies_and_enemies(enemy_add_counter, good_guy_add_counter, enemies, good_guys, goodie, enemy, 'three', '3', resized_w)
    elif score > 500:
        return add_new_goodies_and_enemies(enemy_add_counter, good_guy_add_counter, enemies, good_guys, goodie, enemy, 'two', '2', resized_w)
    elif score < 500:
        if enemy_add_counter == BADDIERATES['one']['ADDNEWBADDIERATE1']:
            enemy_add_counter = 0
            new_enemy = enemy.add_new_figure(resized_w)
            enemies.append(new_enemy)

        if good_guy_add_counter == BADDIERATES['one']['ADDNEWGOODIERATE1']:
            good_guy_add_counter = 0
            new_good = goodie.add_new_figure(resized_w)
            good_guys.append(new_good)

    return enemy_add_counter, good_guy_add_counter


def game_over(screen, font, score, last_score, top_score, hs, resized_w, resized_h):

    draw_text('GAME OVER', font, screen, (resized_w /3), (resized_h / 3))
    draw_text(f'Score: {round(score,2)}', font, screen, (resized_w / 3), (resized_h / 3) + 30)
    draw_text('Press a key to play again.', font, screen,
                 (resized_w / 3) - 80, (resized_h / 3) + 100)

    if score > top_score:
        top_score = score

    if score > hs:
        hs = score
        draw_text('NEW HIGH SCORE!', font, screen,
                (resized_w / 3) - 40, (resized_h / 3) + 60)
        with open(os.path.join(DIRECTORY, HS_FILE), 'w') as f:
            f.write(str(hs) + '\n')
    last_score = score
    pygame.display.update()
    wait_for_player_to_press_key()

    return score, last_score, top_score, hs


def main():
    screen, clock, font, hs = initialization()
    screen
    hero = Hero('Stobko')
    enemy = Enemy('badbi4')
    goodie = Goodie('maimen')
    flash = Flash('flashki')
    shroom = Shroom('shroomski')

    hero_image = hero.get_image()
    hero_rect = hero.get_rectangle()

    last_score = 0.0
    top_score = 0.0
    resized_w, resized_h = pygame.display.get_surface().get_size()

    while True:

        hero_rect.topleft = (resized_w / 2, resized_h - 50)

        score = 0.0
        iteration = 0
        enemy_add_counter = 0
        good_guy_add_counter = 0
        PLAYER_MOVE_RATE = 3

        enemies =[]
        good_guys = []
        flashes = []
        shrooms = []

        move_left = move_right = move_up = move_down = False
        reverse_cheat = False

        while True:

            score += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                    sys.exit()

                if event.type == VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    resized_w, resized_h = pygame.display.get_surface().get_size()

                if event.type == KEYDOWN:
                    if event.key == ord('x'):
                        reverse_cheat = True

                    if event.key == K_LEFT or event.key == ord('a'):
                        move_right = False
                        move_left = True
                    if event.key == K_RIGHT or event.key == ord('d'):
                        move_left = False
                        move_right = True
                    if event.key == K_UP or event.key == ord('w'):
                        move_down = False
                        move_up = True
                    if event.key == K_DOWN or event.key == ord('s'):
                        move_up = False
                        move_down = True

                if event.type == KEYUP:
                    if event.key == ord('x'):
                        reverse_cheat = False
                    if event.key == K_ESCAPE:
                        pygame.QUIT()
                        sys.exit()

                    if event.key == K_LEFT or event.key == ord('a'):
                        move_left = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        move_right = False
                    if event.key == K_UP or event.key == ord('w'):
                        move_up = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        move_down = False

            if not reverse_cheat:
                enemy_add_counter += 1
                good_guy_add_counter += 1

            enemy_add_counter, good_guy_add_counter = check_score(enemy_add_counter, good_guy_add_counter, enemies, good_guys, goodie, enemy, score, resized_w)

            flashes = flash.add_new_flash_to_list(iteration, flashes, resized_w, resized_h)

            shrooms = shroom.add_new_shroom_to_list(iteration, shrooms, resized_w, resized_h)


            hero_rect = hero.move_player_around(move_left, move_right, move_up, move_down, hero_rect, PLAYER_MOVE_RATE, resized_w, resized_h)

            score = move_figure_down(enemies, reverse_cheat, score)
            score = move_figure_down(good_guys, reverse_cheat, score)

            del_figure_past_bottom(enemies, resized_h)
            del_figure_past_bottom(good_guys, resized_h)

            screen.fill(BACKGROUNDCOLOR)

            draw_text('Score: %s' % (round(score,2)), font, screen, 10, 0)
            draw_text('Last: %s' % (round(last_score, 2)), font, screen, 10, 20)
            draw_text('Top: %s' % (round(top_score, 2)), font, screen, 10, 40)
            draw_text('Speed: %s' % (PLAYER_MOVE_RATE), font, screen, 10, 60)

            screen.blit(hero_image, hero_rect)

            draw_figures(screen, enemies)
            draw_figures(screen, good_guys)
            draw_figures(screen, flashes)
            draw_figures(screen, shrooms)

            pygame.display.update()


            score += hero.check_player_hit_goodie(hero_rect, good_guys)
            score += shroom.check_for_collision_with_shroom(hero_rect, shrooms)

            if flash.check_for_collision_with_flash(hero_rect, flashes):
                if random.randint(0,10) % 2 == 0:
                    PLAYER_MOVE_RATE += 1
                else:
                    if PLAYER_MOVE_RATE > 1:
                        PLAYER_MOVE_RATE -= 1
                hero_rect.move_ip(0, PLAYER_MOVE_RATE)

            if enemy.check_for_collision(hero_rect, enemies):
                break

            iteration += 1
            clock.tick(FPS)

        score,last_score, top_score, hs = game_over(screen, font, score, last_score, top_score, hs, resized_w, resized_h)

if __name__ == '__main__':
    main()
