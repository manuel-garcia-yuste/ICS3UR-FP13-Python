#!/usr/bin/env python3

# Created by: Manuel Garcia Yuste
# Created on : December 2019
# Circuit python 13


import ugame
import stage
import board
import neopixel
import time
import random

import constants


def splash_scene():
    # this function is the splash scene game loop

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, 160, 120)

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    # set the layers, items show up in order
    game.layers = [background]
    # render the background and initial location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input

        # update game logic

        # Wait for 1 seconds
        time.sleep(1.0)
        menu_scene()

        # redraw sprite list


def menu_scene():
    # this function is the menu scene

    # an image bank for CircuitPython
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)

    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    text = []

    text1 = stage.Text(width=29, height=14, font=None,
                       palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text1.move(20, 10)
    text1.text("MT Game Studios")
    text.append(text1)

    text2 = stage.Text(width=29, height=14, font=None,
                       palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text2.move(35, 110)
    text2.text("PRESS START")
    text.append(text2)

    # get sound ready
    coin_sound = open("coin.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    # set the layers, items show up in order
    game.layers = text + [background]
    # render the background and initial location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input

        # update game logic
        keys = ugame.buttons.get_pressed()
        # print(keys)

        if keys & ugame.K_START != 0:  # Start button
            game_scene()
            # break

        # redraw sprite list


def game_scene():
    # this function is the game scene

    # game score
    score = 0

    def show_alien():
        # I know this is a function that is using variables outside of itself!
        #   BUT this code is going to be used in 2 places
        # make an alien show up on screen in the x-axis
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < 0:
                aliens[alien_number].move(random.randint(0 +
                                          constants.SPRITE_SIZE,
                                          constants.SCREEN_X -
                                          constants.SPRITE_SIZE),
                                          constants.OFF_TOP_SCREEN)
                break

    # buttons that you want to keep state information on
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # get sound ready
    pew_sound = open("pew2.wav", 'rb')
    boom_sound = open("boom.wav", 'rb')
    crash_sound = open("crash.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")
    # a list of sprites that will be updated every frame
    sprites = []

    # create lasers for when we shoot
    lasers = []
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(image_bank_1, 10, constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_X)
        lasers.append(a_single_laser)

    # set up the NeoPixels to match the # of lasers fired
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 5, auto_write=False)
    for pixel_number in range(0, 5):
        pixels[pixel_number] = (0, 10, 0)
    pixels.show()

    # create aliens
    aliens = []
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(image_bank_1, 8, constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_X)
        aliens.append(a_single_alien)

    # current number of aliens that should be moving down screen
    alien_count = 1
    show_alien()

    # add text at top of screen for score
    score_text = stage.Text(width=29, height=14, font=None,
                            palette=constants.SCORE_PALETTE, buffer=None)
    score_text.clear()
    score_text.cursor(0, 0)
    score_text.move(1, 1)
    score_text.text("Score: {0}".format(score))

    ship = stage.Sprite(image_bank_1, 4, int(constants.SCREEN_X / 2),
                        constants.SCREEN_Y -
                        constants.SPRITE_SIZE)
    sprites.append(ship)  # insert at the top of sprite list

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    # set the layers, items show up in order
    game.layers = sprites + lasers + aliens + [score_text] + [background]
    # render the background and initial location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        # print(keys)

        if keys & ugame.K_X != 0:  # A button
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]

        # update game logic

        # if right D-Pad is pressed
        if keys & ugame.K_RIGHT != 0:
            # if ship moves off right screen, move it back
            if ship.x > constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.x = constants.SCREEN_X - constants.SPRITE_SIZE
            # else move ship right
            else:
                ship.move(ship.x + constants.SHIP_SPEED, ship.y)

        # if left D-Pad is pressed
        if keys & ugame.K_LEFT != 0:
            # if ship moves off left screen, move it back
            if ship.x < 0:
                ship.x = 0
            # else move ship left
            else:
                ship.move(ship.x - constants.SHIP_SPEED, ship.y)

        if keys & ugame.K_UP != 0:
            if ship.y < 0:
                ship.move(ship.x, 0)
            else:
                ship.move(ship.x, ship.y - constants.SHIP_SPEED)
            pass

        if keys & ugame.K_DOWN != 0:
            if ship.y > constants.SCREEN_Y - constants.SCREEN_GRID_Y:
                ship.move(ship.x, constants.SCREEN_Y - constants.SPRITE_SIZE)
            else:
                ship.move(ship.x, ship.y + constants.SHIP_SPEED)
            pass

        # if A Button (fire) is pressed
        if a_button == constants.button_state["button_just_pressed"]:
            # fire a laser, if we have enough power
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:
                    lasers[laser_number].move(ship.x, ship.y)
                    sound.stop()
                    sound.play(pew_sound)
                    break

        # each frame move the lasers, that have been fired, up

        # make all the neopixels yellow
        lasers_moving_counter = -1
        for pixel_number in range(0, 5):
            pixels[pixel_number] = (0, 10, 0)

        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                lasers[laser_number].move(lasers[laser_number].x,
                                          lasers[laser_number].y -
                                          constants.LASER_SPEED)
                lasers_moving_counter = lasers_moving_counter + 1
                pixels[lasers_moving_counter] = (10, 10 - (2 *
                                                 lasers_moving_counter + 2), 0)
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)
        if lasers_moving_counter == 4:
            for pixel_number in range(0, 5):
                pixels[pixel_number] = (10, 0, 0)
        pixels.show()

        # each frame move the aliens down the screen
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:  # meaning it is on the screen
                aliens[alien_number].move(aliens[alien_number].x,
                                          aliens[alien_number].y +
                                          constants.ALIEN_SPEED)
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)
                    show_alien()  # make it randomly show up at top again

        # each frame check if any of the lasers are touching any of the aliens
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                for alien_number in range(len(aliens)):
                    if aliens[alien_number].x > 0:

                        # the first 4 numbers are the coordinates of A box
                        if stage.collide(lasers[laser_number].x + 6,
                                         lasers[laser_number].y + 2,
                                         lasers[laser_number].x + 11,
                                         lasers[laser_number].y + 12,
                                         aliens[alien_number].x + 1,
                                         aliens[alien_number].y,
                                         aliens[alien_number].x + 15,
                                         aliens[alien_number].y + 15):
                            # you hit an alien
                            aliens[alien_number].move(constants.OFF_SCREEN_X,
                                                      constants.OFF_SCREEN_Y)
                            # add 1 to the score
                            score += 1
                            score_text.clear()
                            score_text.cursor(0, 0)
                            score_text.move(1, 1)
                            score_text.text("Score: {0}".format(score))
                            # this will freeze the screen for a split second
                            game.render_block()
                            # play sound effect
                            sound.stop()
                            sound.play(boom_sound)
                            show_alien()
                            show_alien()
                            alien_count = alien_count + 1

        # each frame check if any of the aliens are touching the ship
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                if stage.collide(aliens[alien_number].x + 1,
                                 aliens[alien_number].y,
                                 aliens[alien_number].x + 15,
                                 aliens[alien_number].y + 15,
                                 ship.x, ship.y,
                                 ship.x + 15, ship.y + 15):
                    # alien hit the ship
                    sound.stop()
                    sound.play(crash_sound)
                    for pixel_number in range(0, 5):
                        pixels[pixel_number] = (25, 0, 25)
                    pixels.show()
                    # Wait for 1 seconds
                    time.sleep(4.0)
                    # need to release the NeoPixels
                    pixels.deinit()
                    sound.stop()
                    game_over_scene(score)

        # redraw sprite list
        game.render_sprites(sprites + lasers + aliens)
        game.tick()  # wait until refresh rate finishes


def game_over_scene(final_score):
    # this function is the game over scene
    # an image bank for CircuitPython
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)

    text = []

    text0 = stage.Text(width=29, height=14, font=None,
                       palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text0.move(22, 20)
    text0.text("Final Score: {:0>2d}".format(final_score))
    text.append(text0)

    text1 = stage.Text(width=29, height=14, font=None,
                       palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text1.move(43, 60)
    text1.text("GAME OVER")
    text.append(text1)

    text2 = stage.Text(width=29, height=14, font=None,
                       palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text2.move(32, 110)
    text2.text("PRESS SELECT")
    text.append(text2)

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    # set the layers, items show up in order
    game.layers = text + [background]
    # render the background and initial location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input

        # update game logic
        keys = ugame.buttons.get_pressed()
        # print(keys)

        if keys & ugame.K_SELECT != 0:  # Start button
            keys = 0
            menu_scene()
            # break

        # redraw sprite list


if __name__ == "__main__":
    splash_scene()
