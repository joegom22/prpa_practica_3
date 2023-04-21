# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:27:27 2023

@author: USUARIO
"""
import os

#varias variables que vamos a usar
WIDTH = 1000
HEIGHT = 650
FPS = 30
SIZE = (WIDTH,HEIGHT)
TITLE = 'juego paralela'
friction = -0.20
player_acc = 3

# definimos colores
BLACK = (0, 0, 0)
BLUE = (180, 255, 255)

#posiciones de los inicios para los 2 jugadores
inicio1 = [100,60]
inicio2 = [200,60]
#posiciones de las paredes
paredes = [[130,307,278,137],[408,423,161,21],
           [130,145,278,90],[315,97,93,48],
           [525,97,208,138],[479,306,91,46],
           [758,540,200,110],[805,10,155,1000],
           [50,0,910,26],[40,0,20,1000],
           [45,516,130,140],[643,307,90,138],
           [270,516,416,67]]
#posiciones de las banderas 
banderas = [[200,560],[580,350],[750,100]]



#imagenes que vamos a utilizar
game_folder = os.path.dirname(__file__)
path = os.path.join(game_folder,'camino2.png')
persona1 = os.path.join(game_folder,'p1_front.png')
persona2 = os.path.join(game_folder,'p2_front.png')
bandera_roja = os.path.join(game_folder,'flagRed.png')
