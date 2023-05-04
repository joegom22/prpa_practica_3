"""
Created on Wed Apr 19 10:27:27 2023
@author: USUARIO
"""
import os

#varias variables que vamos a usar
WIDTH = 850
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
inicio1 = [100,70]
inicio2 = [200,70]
#posiciones de las paredes
paredes = [[90,329,278,137],[368,445,161,21],
           [90,167,278,90],[275,119,93,48],
           [485,119,208,138],[439,328,91,46],
           [718,562,200,110],[765,47,155,1000],
           [0,47,910,1],[0,47,20,1000],
           [2,538,130,140],[603,329,90,138],
           [230,538,416,67]]
#posiciones de las banderas 
banderas = [[200,560],[580,350],[750,100], [750,350], [700, 560]]



#imagenes que vamos a utilizar
game_folder = os.path.dirname(__file__)
path = os.path.join(game_folder,'camino2.png')
persona1 = os.path.join(game_folder,'p1_front.png')
persona2 = os.path.join(game_folder,'p2_front.png')
bandera_roja = os.path.join(game_folder,'flagRed.png')
fin_p0=os.path.join(game_folder, 'Fin_partida_player0.png')
fin_p1=os.path.join(game_folder, 'Fin_partida_player1.png')
