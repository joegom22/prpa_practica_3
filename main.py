# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:34:51 2023

@author: USUARIO
"""

import pygame as pg #importamos el módulo pygame
import settings as st #importamos el archivo con todos los parámetros
import sprites as sp #importamos el archivo con todos los sprites (elementos que hay en el juego)
import socket
import json

#Definimos la clase para el Juego
class Game:
    #lo inicializamos
    def __init__(self):
        #inicializamos el módulo pygame (que lo hemos llamado pg)
        pg.init()
        pg.mixer.init()
        
        #definimos el tamaño de la pantalla de juego
        self.screen = pg.display.set_mode(st.SIZE)
        
        #le ponemos un título al juego
        pg.display.set_caption(st.TITLE)
        
        #definimos el reloj (para los FPS)
        self.clock = pg.time.Clock()
        
        #definimos la variable para ver cuando estamos jugando (si == False, se para el juego)
        self.running = True
        
        #atributo para el contador de banderas e ir añadiendolas
        self.contador_banderas = 0
        
    #función para crear un nuevo juego
    def new(self):
        #creamos un Grupo para añadir todos los sprites (los sprites son los elementos del juego)
        self.all_sprites = pg.sprite.Group()
        
        #creamos y añadimos al Grupo el camino (la imagen del fondo)
        self.path = sp.Path()
        self.all_sprites.add(self.path)
        
        #Creamos y añadimos al Grupo los jugadores
        self.player1 = sp.Player(1)
        #self.player2 = sp.Player(2)
        self.all_sprites.add(self.player1)
        #self.all_sprites.add(self.player2)
        
        #Creamos y añadimos al Grupo las paredes
        self.paredes = pg.sprite.Group()
        for pared in st.paredes:
            self.pared = sp.Pared(pared[0],pared[1],pared[2],pared[3])
            self.paredes.add(self.pared)
            self.all_sprites.add(self.pared)
        
        #Creamos y añadimos al Grupo las banderas
        self.banderas = pg.sprite.Group()
        self.añade_bandera()
        
        #Iniciamos el juego
        self.run()
        
    #Función para añadir una bandera al juego
    def añade_bandera(self):
        # selecciona una bandera de la lista de banderas de settings
        self.bandera = sp.Flags(st.banderas[self.contador_banderas][0],st.banderas[self.contador_banderas][1])
        
        #añade la bandera al Grupo 
        self.banderas.add(self.bandera)
        self.all_sprites.add(self.bandera)
        
        #como hemos puesto 1 bandera, sube el contador, para que así la siguiente bandera que añada sea la contador+1
        self.contador_banderas += 1

    #Función que hace funcionar el juego
    def run(self):
        self.playing = True
        while self.playing:
            #se ven los FPS
            self.clock.tick(st.FPS)
            
            #primeros ocurren los events, luego los updates y luego el draw (mas explicación en cada función)
            self.events()
            self.update()
            self.draw()
    
    #Función que hace todos las actualizaciones del juego
    def update(self):
        #Actualiza los sprites
        self.all_sprites.update()
        
        #Primero vemos si ha habido una colisión de algun jugador con alguna pared.
        #En caso afirmativo, le devuelve al inicio
        
        hits_paredes_p1 = pg.sprite.spritecollide(self.player1,self.paredes,False)        
        if hits_paredes_p1:
            self.player1.pos.x = st.inicio1[0]
            self.player1.pos.y = st.inicio1[1]
            
        #hits_paredes_p2 = pg.sprite.spritecollide(self.player2,self.banderas,False)
        #if hits_paredes_p2:
        #    self.player2.pos.x = st.inicio2[0]
        #    self.player2.pos.y = st.inicio2[1]
        
        
        #Despues vemos si algún jugador ha tocado alguna bandera.
        #En caso afirmativo, elimina la bandera del juego con el comando kill y
        #también añade otra bandera
        #Si un jugador toca 2 banderas (es decir, self.player.score == 2, se acaba el juego)
        
        
        hits_banderas_p1 = pg.sprite.spritecollide(self.player1,self.banderas,False)
        if self.player1.vel.x > 0 or self.player1.vel.y > 0:
            if hits_banderas_p1:
                hits_banderas_p1[0].kill()
                self.añade_bandera()
                self.player1.score += 1
        if self.player1.score == 2:
            self.playing = False
            self.running = False
        #hits_banderas_p2 = pg.sprite.spritecollide(self.player2,self.banderas,False)
        #if self.player2.vel.x > 0 or self.player2.vel.y > 0:
        #    if hits_banderas_p2:
        #        hits_banderas_p2[0].kill()
        #        self.añade_bandera()
        #        self.player1.score += 1
        #if self.player2.score == 2:
        #        self.playing = False
        #        self.running = False
            
            
            
    #Función que dice los eventos que hay. En nuestro caso,
    #el único evento es si se pulsa a la 'X' de la esquina superior derecha, en cuyo caso se acaba el juego
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    #Actualiza lo que se ve por pantalla con el comando flip
    def draw(self):
        self.screen.fill(st.BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        
#Acepta 2 jugadores y ejecuta el juego
def main():
    n=0
    manager = Manager()
    host = '0.0.0.0'
    port = 5001
    mysocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind((host,port))
    while n<2:
	    mysocket.listen(10)
	    print('Listening')
	    conn, addr = mysocket.accept()
	    print('accepted')
	    n += 1
	    if n ==1:
		    n_player = 0
		    players = [None, None]
		    game = Game(manager)
		    gameinfo=game.get_info()
		    conn.send(str(n_player).encode())
		    conn.send(json.dumps(gameinfo).encode())
		    players[n_player] = Process(target=player, args=(n_player, conn, game))
	    else:
	        n_player = 1
	        game = Game(manager)
	        conn.send(str(n_player).encode())
	        gameinfo=game.get_info()
	        conn.send(json.dumps(gameinfo).encode())
	        players[n_player] = Process(target=player, args=(n_player, conn, game))
            
	players[0].start()
	players[1].start()
	n_player = 0
	players = [None, None]
	game = Game(manager)
	        
    g = Game()
    try:
        while g.running:
            g.new()
    finally:
        pg.quit()



if __name__ == '__main__':
    main()
