# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 12:14:08 2022

@author: nuria


Ideas #todo
- Add either a disgusting image, or a cute image, to make u be not nearby screen
"""
from __future__ import print_function
from WebcamVideoStream import WebcamVideoStream
from threading import Thread
import pygame
import os
import time
import cv2 as cv
import argparse


#todo - remove random
import random

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


vs = WebcamVideoStream(src=0).start()
stream = cv.VideoCapture(0, cv.CAP_DSHOW)
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
def updateGUI():
    clock.tick(60)
Thread(target=updateGUI, args=()).start()

toggle = False
while True:
    ret, frame = stream.read()
    width = detectWidth(frame)
    print(width)
    if width > 180:
        pygame.init()
        screen.fill((200,0,0))
        warning = True
    else:
        screen.fill((255, 255, 255))
        warning = False

    pygame.display.flip()


    if cv.waitKey(1) & 0xFF == ord('q'):
        pygame.quit()
        break

stream.release()
cv.destroyAllWindows()
