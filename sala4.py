# -*- coding: utf-8 -*-
"""
Created on Fri May  5 14:25:24 2023

@author: USUARIO
"""

from multiprocessing.connection import Listener, Client
from multiprocessing import Process, Manager, Value, Lock
import pygame as pg #importamos el módulo pygame
import settings as st #importamos el archivo con todos los parámetros
import socket
import random
import traceback, sys, os, json
DELTA = 30
class Player():
    def __init__(self, n_player):
        """
        Función de la clase Player que inicializa al jugador dándole como número de jugador un valor dado.
        Le coloca en su posición inicial y pone su velocidad, puntuación y aceleración a cero
        
        args
            self
            n_player: int --> número de jugador
        """        
        self.n_player = n_player
        if self.n_player == 0:
            self.pos = [st.inicio1[0],st.inicio1[1]]
            self.vel = [0,0]
            self.acc = [0,0]
            
            #la puntuación que lleva el jugador
            self.score = 0
        else:
            self.pos = [st.inicio2[0],st.inicio2[1]]
            self.vel = [0,0]
            self.acc = [0,0]
            
            #la puntuación que lleva el jugador
            self.score = 0

    def get_pos(self):
        """
        Función de la clase Player que devuelve la posición del jugador
        
        args
            self
        """
        return self.pos
    
    def set_pos(self, pos):
        """
        Función de la clase Player que cambia la posición del jugador por una dada
        
        args
            self
            pos: [int, int] --> nueva posición
        """    
        self.pos = pos    
    
    def get_number(self):
        """
        Función de la clase Player que devuelve el número del jugador
        
        args
            self
        """       
        return self.n_player
        
    def moveDown(self):
        """
        Función de la clase Player que desplaza al jugador hacia abajo una cantidad delta.
        Además se asegura de que si el jugador se sale de la pantalla vuelve al inicio.
        
        args
            self
        """
        self.pos[1] += DELTA
        if self.pos[1]>650:
        	self.pos = [st.inicio1[0],st.inicio1[1]]
    
    def moveUp(self):
        """
        Función de la clase Player que desplaza al jugador hacia arriba una cantidad delta.
        Además se asegura de que si el jugador se sale de la pantalla vuelve al inicio.
        
        args
            self
        """        
        self.pos[1] -= DELTA
        if self.pos[1]<0:
        	self.pos = [st.inicio1[0],st.inicio1[1]]
    
    def moveLeft(self):
        """
        Función de la clase Player que desplaza al jugador hacia la izquierda una cantidad delta.
        
        args
            self
        """  
        self.pos[0] -= DELTA
    
    def moveRight(self):
        """
        Función de la clase Player que desplaza al jugador hacia la derecha una cantidad delta.
        
        args
            self
        """  
        self.pos[0] += DELTA
    
    def inicio(self,n_player):
        """
        Función de la clase Player que coloca al jugador en su posición inicial.
        
        args
            self
            n_player: int --> número de jugador
        """          
        if n_player == 0:
            self.pos = st.inicio1
        else:
            self.pos = st.inicio2
    
    def __str__(self):
        """
        Función que sirve para visualizar el estado del jugador por pantalla
        
        args
            self
        """
        return f"P<{self.n_player}, {self.pos}>"
        
class Flag():
    def __init__(self, x, y):
        """
        Función de la clase Flag que inicializa una bandera en una posición dada
        
        args
            self
            x: int --> coordenada x de la posición
            y: int --> coordenada y de la posición
        """ 
        self.pos = [x,y]
    
    def get_pos(self):
        """
        Función de la clase Flag que devuelve la posición de la bandera
        
        args
            self
        """ 
        return self.pos
    
    def __str__(self):
        """
        Función que sirve para visualizar el estado de la bandera por pantalla
        
        args
            self
        """
        return f"F<{self.pos}>"
        
class Wall():
    def __init__(self, x, y, w, h):
        """
        Función de la clase Wall que inicializa un muro en una posición dada y con una anchura y una altura dadas
        
        args
            self
            x: int --> coordenada x de la posición
            y: int --> coordenada y de la posición
            w: int --> anchura
            h: int --> altura
        """ 
        self.pos = [x,y]
        self.measures = [w, h]
    
    def get_pos(self):
        """
        Función de la clase Wall que devuelve la posición del muro
        
        args
            self
        """ 
        return self.pos
    
    def get_measures(self):
        """
        Función de la clase Wall que devuelve las medidas del muro
        
        args
            self
        """ 
        return self.measures
        
    def __str__(self):
                """
        Función que sirve para visualizar el estado del muro por pantalla
        
        args
            self
        """
        return f"W<{self.pos}>"
        

class Game():
    def __init__(self, manager):
        """
        Función de la clase Game que inicializa el juego. Crea una lista con las banderas, con la bandera visible, con los jugadores y con los muros.
        Crea también la puntuación, el cronómetro, un lock para ayudarnos a evitar concurrencias no deseadas, un valor de si estamos jugando (0 es no, 1 es sí).
        
        args
            self
            manager: manager
        """
        self.players = manager.list( [Player(0), Player(1)] )
        self.lista = []
        self.flags = manager.list()

        for i in st.banderas:
            self.flags.append(Flag(i[0],i[1]))
        lista2 = []
        for i in st.paredes:
            lista2.append(Wall(i[0],i[1],i[2],i[3]))
        self.walls = manager.list(lista2)

        self.score = manager.list([0,0])
        self.running = Value('i', 1)# 1 running
        self.lock = Lock()
            
    def get_player(self, n_player):
        """
        Función de la clase Game que dado un número de jugador devuelve el jugador con dicho número
        
        args
            self
            n_player: int --> número de jugador
        """
        return self.players[n_player]
        
    def get_wall(self, n):
    	"""
        Función de la clase Game que dado un índice devuelve el muro en esa posición en la lista de muros
        
        args
            self
            n: int --> índice
        """
        return self.walls[n]
    	
    def get_flag(self):
        """
        Función de la clase Game que devuelve la bandera visible
        
        args
            self
        """
        return self.flags[0]
    
    def get_score(self):
        """
        Función de la clase Game que devuelve la puntuación
        
        args
            self
        """
        return list(self.score) 

    def is_running(self):
        """
        Función de la clase Game que devuelve cierto o falso en función de si el juego sigue o debe parar resp.
        
        args
            self
        """
        return self.running.value == 1

    def stop(self):
        """
        Función de la clase Game que cambia el valor de running para que el juego se detenga
        
        args
            self
        """
        self.running.value = 0 
        
    def moveUp(self, n_player):
        """
        Función de la clase Game que mueve al jugador hacia arriba llamando a la correspondiente función de la clase Player.
        Luego actualiza ese jugador.
        El lock impide la concurrencia
        
        args
            self
            n_player: int --> numero de jugador
        """
        self.lock.acquire()
        p = self.players[n_player]
        p.moveUp()
        self.players[n_player]=p
        self.lock.release()
        
    def moveDown(self, n_player):
        """
        Función de la clase Game que mueve al jugador hacia abajo llamando a la correspondiente función de la clase Player.
        Luego actualiza ese jugador.
        El lock impide la concurrencia
        
        args
            self
            n_player: int --> numero de jugador
        """
        self.lock.acquire()
        p = self.players[n_player]
        p.moveDown()
        self.players[n_player]=p
        self.lock.release()
                
    def moveLeft(self, n_player):
        """
        Función de la clase Game que mueve al jugador hacia la izquierda llamando a la correspondiente función de la clase Player.
        Luego actualiza ese jugador.
        El lock impide la concurrencia
        
        args
            self
            n_player: int --> numero de jugador
        """
        self.lock.acquire()   
        p = self.players[n_player]
        p.moveLeft()
        self.players[n_player]=p
        self.lock.release()
                
    def moveRight(self, n_player):
        """
        Función de la clase Game que mueve al jugador hacia la derecha llamando a la correspondiente función de la clase Player.
        Luego actualiza ese jugador.
        El lock impide la concurrencia
        
        args
            self
            n_player: int --> numero de jugador
        """
        self.lock.acquire()
        p = self.players[n_player]
        p.moveRight()
        self.players[n_player]=p
        self.lock.release()
   
    def remove_flag(self,manager,flag_pos):
        """
        Función de la clase Game que elimina la bandera que era visible
        
        args
            self
            manager: manager
        """
        j = 0
        for i in self.flags:
            if i.get_pos() == flag_pos:
                self.flags.pop(j)
                break
            j += 1
            
    def win_flag(self, manager, n_player,flag_pos):
        """
        Función de la clase Game que elimina la bandera de la posición dada, suma 1 a la puntuación del jugador con número el dado y, tras actualizar los jugadores, 
        comprueba si se ha llegado a la puntuación necesaria para ganar, si es así termina el juego.
        El lock evita la concurrencia, ya que 2 jugadores no pueden ganar bandera a la vez
        
        args
            self
            manager: manager
            n_player: int --> número del jugador
        """
        self.lock.acquire()
        self.remove_flag(manager,flag_pos)
        p = self.players[n_player]
        p.score += 1
        self.players[n_player] = p
        self.score[n_player] += 1
        p = self.players[0]
        p.inicio(0)
        self.players[0] = p
        q = self.players[1]
        q.inicio(1)
        self.players[1] = q
        if self.players[n_player].score == 3:
            print("fin")
            self.running.value = 0
        self.lock.release()
                
    def collide_wall(self, manager, n_player):
        """
        Función de la clase Game que devuelve al jugador con número el dado a su posición inicial
        
        args
            self
            manager: manager
            n_player: int --> número del jugador
        """
        self.lock.acquire()
        if n_player == 0:
            p = self.players[n_player]
            p.inicio(n_player)
            self.players[n_player]=p

        else:
            p = self.players[n_player]
            p.inicio(n_player)
            self.players[n_player]=p

        self.lock.release()  
         
    def get_info(self):
        """
        Función de la clase Game que nos devuelve en un diccionario la información relevante del juego.
        Las posiciones de ambos jugadores, la posición de la bandera visible, la de los muros, la puntuación y si el juego debe seguir corriendo o debe parar.
        
        args
            self
        """
        lista = []
        for i in self.walls:
            lista.append((i.get_pos(),i.get_measures()))
        flags = []
        for i in self.flags:
            flags.append(i.get_pos())
        info = {"pos_player_0": self.players[0].get_pos(),"pos_player_1": self.players[1].get_pos(),"pos_flag": flags,"walls": lista,"score": list(self.score),"is_running": self.running.value == 1}
        return info
    
def __str__(self):
        """
        Función de la clase Game que sirve para visualizar por pantalla el estado de ambos jugadores y si el juego debe seguir corriendo o no.
        
        args
            self
        """
        return f"G<{self.players[0]}:{self.players[1]}:{self.running.value}>"
    
def player(n_player, manager, conn, game):
    """
    Función que actuará como proceso del jugador.
    Comienza y recibe la información del juego, mientras la orden no sea parar continuará realizando acciones.
    
    args
        n_player: int --> número del jugador
        manager: manager
        conn: connection
        game: game
    """
    try:
        print(f"starting player {n_player}")
        gameinfo = game.get_info()
        conn.send(gameinfo)
        while game.is_running():
            command = ""
            while command != "next":
                command = conn.recv()
                if command == "up":
                    game.moveUp(n_player)
                elif command == "down":
                    game.moveDown(n_player)
                elif command == "left":
                    game.moveLeft(n_player)
                elif command == "right":
                    game.moveRight(n_player)
                elif command[0] == "flag":
                    print('ccccc')
                    game.win_flag(manager, n_player,command[1])
                elif command == "wall":
                    game.collide_wall(manager, n_player)
                elif command == "quit":
                    game.stop()
            gameinfo = game.get_info()
            conn.send(gameinfo)
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {game}")   

def main():
    """
    Función principal sn argumentos. Inicializa la escucha en una ip y un puerto y acepta 2 conexiones, que convierte en procesos de la función player y les manda la información del juego.
   
    """
    manager = Manager()
    host = '0.0.0.0'
    port = 5000
    try:
        with Listener((host, port),
                      authkey=b'secret password') as listener:
            n_player = 0
            players = [None, None]
            game = Game(manager)
            while True:
                print(f"accepting connection {n_player}")
                conn = listener.accept()
                gameinfo = game.get_info()
                conn.send(n_player)
                conn.send(gameinfo)
                players[n_player] = Process(target=player,
                                            args=(n_player, manager, conn, game))
                n_player += 1
                if n_player == 2:
                    gameinfo = game.get_info()
                    conn.send(gameinfo)
                    players[0].start()
                    players[1].start()
                    n_player = 0
                    players = [None, None]
                    game = Game(manager)

    except Exception as e:
        traceback.print_exc()

if __name__=='__main__':
    main()  
