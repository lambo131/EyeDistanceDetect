# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 12:14:08 2022

@author: nuria


Ideas #todo
- Add either a disgusting image, or a cute image, to make u be not nearby screen
"""

import pygame
import os
import time

#todo - remove random
import random


def pygame_loop():
    pygame.init()
    screen_width = 700
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame_icon_png = "Eyes.png"    #icon of pygame. Must be 32x32 pixels

    font_30 = pygame.font.SysFont("calibri", 30)
    font_18 = pygame.font.SysFont("calibri", 30)

    def write_message(message, color = (0,0,0), rectangle=[0,0], font=font_18, update = True, centered = False):
        mesg = font.render(message, True, color)
        if centered:
            w,h = rectangle
            rectangle = [w-mesg.get_width()/2,h]
        screen.blit(mesg, rectangle)
        if update:
            pygame.display.update()

    def RedScreen():
        screen.fill((200,0,0))
        write_message("you are too close to the screen!", color = (255,255,255), rectangle=(screen_width/2, screen_height/2), centered=True, font=font_30)

    Open = True
    while Open: 
        RedScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Open = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    Open = False
            
    pygame.quit()    


def AppLoop():
    PygameLoop = True
    
    min_distance = 40
    while PygameLoop:
        
        #add the distance function here
        distance = random.randint(0,100)
        if distance < min_distance:
            pygame_loop()
        
        time.sleep(15)
        
            
AppLoop()