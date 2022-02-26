from threading import Thread

from TargetVision import Vision
from TargetTrack import Target

import time
import pygame
pygame.init()

dis = pygame.display.set_mode((500, 500))

targetVision = Vision()
ball = Target(diameter="35")
ballX = 0
ballZ = 0
clock = pygame.time.Clock()

def update():
    clock.tick(60)

Thread(target=update, args=()).start()
while True:
    targetVision.captureVision()
    ballX, ballY, ballDiameter = targetVision.getBallInformation()
    targetVision.showVision()
    ball.updateStatus(ballX, ballY, ballDiameter, targetVision.getFps())
    ball.setZ_pos()
    ball.setX_pos()
    ball.setZ_velocity()
    ball.setX_velocity()
    print(ball.getX(),ball.getZ())
    ballX = ball.getX()
    ballZ = ball.getZ()
    # print(ball.getTargetDistance())
    # print(ball.getZVelocity())
    # ball.printTargetInformation()
    # ball.getBallTimeToCenter()
    # ball.getBall300To100Time()
    # print(ball.getX_velocity())

    dis.fill((0, 0, 0))
    pygame.draw.rect(dis, (255, 0, 0), pygame.Rect(250+ballX, ballZ/3, 30, 30))

    pygame.display.flip()

pygame.quit()