# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 12:14:08 2022

@author: nuria



#todo
- change so that it does not pop up two times if I am already away (maybe sleep for 1sec? lets try)
"""
from __future__ import print_function
from threading import Thread
import pygame
import datetime
import time

import os
import json
import cv2 as cv
import argparse
import ctypes  # An included library with Python install.


stream = cv.VideoCapture(0, cv.CAP_DSHOW)
pygame.init()
screen_width, screen_height = 500, 500
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

font_30 = pygame.font.SysFont("calibri", 30)
font_18 = pygame.font.SysFont("calibri", 18) 
font_16 = pygame.font.SysFont("calibri", 16)


filepath = os.path.dirname(__file__)


class button():
    def __init__(self, color, x,y,width,height, text='', font=font_30):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

    def draw(self,screen):
        #Call this method to draw the button on the screen            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0,5)
        
        if self.text != '':
            text = self.font.render(self.text, 1, (255,255,255))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

def change_button_color(button_key, pos, default_color=(0,0,0), isOver_color=(0,0,255)):
    if button_key.isOver(pos):
        button_key.color = isOver_color
    else:
        button_key.color = default_color
    button_key.draw(screen)
    pygame.display.update()


def detectWidth(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    faces = face_cascade.detectMultiScale(frame_gray,1.3,5)
    width = 0
    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        frame = cv.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y + h, x:x + w]
        # -- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)

        for (x2, y2, w2, h2) in eyes:

            eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)

        width = w
    cv.imshow('Capture - Face detection', frame)
    return width

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def write_json(average_distance, num_popups, time_opened):
    YEAR        = datetime.date.today().year
    MONTH       = datetime.date.today().month
    DATE        = datetime.date.today().day
    HOUR        = datetime.datetime.now().hour
    MINUTE      = datetime.datetime.now().minute
    SECONDS     = datetime.datetime.now().second


    json_dict = {
        "h_{}_m_{}".format(HOUR,MINUTE): {
            "average_distance" : average_distance,
            "num_popups": num_popups,
            "time_opened": time_opened
            }
        }
        
    json_file = open(os.path.join(filepath,"dict.json"),"w")
    json.dump(json_dict, json_file)
    json_file.close()

def pygame_intro():

    def write_message(message, color = (0,0,0), rectangle=[0,0], font=font_18, update = True, centered = False):
        mesg = font.render(message, True, color)
        if centered:
            w,h = rectangle
            rectangle = [w-mesg.get_width()/2,h]
        screen.blit(mesg, rectangle)
        if update:
            pygame.display.update()
    
    def Initial_Screen():
        screen.fill((255,255,255))
        write_message("Welcome to Screen distance tracker!", rectangle=(screen_width/2, 20), centered=True, font=font_18)
        write_message("While open, this app will warn you if you are too close to the screen", rectangle=(screen_width/2, 50), centered=True, font=font_16)
        write_message("This link will show you what will happen if you do this too often", rectangle=(screen_width/2, 80), centered=True, font=font_16)
        write_message("Do you want to start the app?", rectangle=(screen_width/2, 110), centered=True, font=font_16)
        
        button_off = button((255,0,0),220,220,50,50,text="OFF")
        button_off.draw(screen)
        pygame.display.update()
        
        Open = True
        while Open:
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    if button_off.isOver(pos):
                        if button_off.color == (255,0,0):
                            button_off = button((100,0,0),220,220,50,50,text="OFF")
                            button_off.draw(screen)
                            pygame.display.update()
                    elif button_off.color == (100,0,0):
                        button_off = button((255,0,0),220,220,50,50,text="OFF")
                        button_off.draw(screen)
                        pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_off.color == (100,0,0):
                        button_off = button((0,255,0),220,220,50,50,text="ON")
                        button_off.draw(screen)
                        pygame.display.update()
                        time.sleep(1)
                        Open = False
                
                if event.type == pygame.QUIT:
                    Open = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Open = False
                    if event.key == pygame.K_q:
                        Open = False
                        
    
    Initial_Screen()
                        
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default= cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default= cv.data.haarcascades + 'haarcascade_eye.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)
camera_device = args.camera


def updateGUI():
    clock.tick(60)
    

pygame_intro()
button_off = button((0,255,0),220,220,50,50,text="ON")
button_off.draw(screen)

Thread(target=updateGUI, args=()).start()


start = time.time()
distance_list=[]
num_popups = 0

Close = False
toggle = False
while True:
    start_close_screen = time.time()
    still_close_screen = time.time()
    
    ret, frame = stream.read()
    width = detectWidth(frame)
    distance_list.append(width)

    if width > 180:
        Mbox('Get away!', 'You are too close to the screen', 0)
        num_popups +=1
        startloop = time.time()
    
    
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if button_off.isOver(pos):
                if button_off.color == (0,255,0):
                    button_off = button((0,100,0),220,220,50,50,text="ON")
                    button_off.draw(screen)
                    pygame.display.update()
            elif button_off.color == (0,100,0):
                button_off = button((0,255,0),220,220,50,50,text="ON")
                button_off.draw(screen)
                pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_off.color == (0,100,0):
                button_off = button((255,0,0),220,220,50,50,text="OFF")
                print("off")
                button_off.draw(screen)
                pygame.display.update()
                Close = True
        
        if event.type == pygame.QUIT:
            Close = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                Close = True
            if event.key == pygame.K_q:
                Close = True
    
    pygame.display.flip()
    
    if (cv.waitKey(1) & 0xFF == ord('q')) or Close == True:
        pygame.quit()
        break

average_distance = 0
end = time.time()
time_opened = end - start
write_json(average_distance, num_popups, time_opened)
stream.release()
cv.destroyAllWindows()
