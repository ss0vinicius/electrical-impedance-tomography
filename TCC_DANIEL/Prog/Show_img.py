from operator import delitem, truediv
from random import randint
from time import sleep
from turtle import Screen, delay
import math
import pygame
from pygame.locals import *
import csv


'''
---------------------------------------------------

Definição de parametros

---------------------------------------------------
'''

width = 800
height = width
radius = height/2
point = 10

#------------------------------------------

with open('Cord.csv', 'r') as ficheiro:
    reader = csv.reader(ficheiro, delimiter=',',quoting= csv.QUOTE_NONNUMERIC)

    maiorX = 1
    maiorY = 1

    for linha in reader:

        tx = float(linha[0])
        ty = float(linha[1])
        if(tx< maiorX):
            maiorX = tx

        if(ty< maiorY):
            maiorY = ty
    
    print("_______________________________________________________________\n\n\n")
    print(f"maior X {maiorX}\n")
    print(f"maior y {maiorY}\n")
    print("_______________________________________________________________\n\n\n")

    menorX = maiorX

    menorY = maiorY

    for linha in reader:

        tx = float(linha[0])
        print(tx)
        ty = float(linha[1])
        print(ty)
        if(tx < menorX):
             menorX = tx

        if(ty < menorY):
            menorY= ty


    print(f"menor X _>{menorX}\n")
    print(f"menor y {menorY}\n")
"""


while True:
    sleep(0.5)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    
    screen.fill((0,0,0))

    pygame.draw.circle(screen,(255,255,255),(width/2,height/2),radius)

    for i in range(1000):

        y = randint(0,height)
        x = randint(0,width)
        if pow(x-width/2,2)+pow(y-height/2,2) <= pow(radius - 10,2):
            #pygame.draw.rect(screen,(randint(0,254),randint(0,254),randint(0,254)),(x,y,point,point))

    pygame.display.update()
    
    """