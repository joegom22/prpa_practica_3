# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:31:40 2023

@author: USUARIO
"""

import pygame as pg
import settings as st

#esto sirve para definir un vector y asi poder poner aceleración y velocidad
vec = pg.math.Vector2

#Definimos la clase para el Jugador
class Player(pg.sprite.Sprite):
    #lo inicializamos
    def __init__(self,player_number):
        
        #vemos si es el jugador 1 o 2
        self.player_number = player_number
        
        if self.player_number == 1:
            pg.sprite.Sprite.__init__(self)
            
            #cargamos su imagen (la imagen del 'alien')
            self.image = pg.image.load(st.persona1).convert()
            
            #creamos un rectangulo alrededor suyo
            self.rect = self.image.get_rect()
            
            #esto sirve para que se defina la silueta bien
            self.image.set_colorkey(st.BLACK)
            
            #definimos la posición, velocidad y aceleración con vec
            self.pos = vec(st.inicio1[0],st.inicio1[1])
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            
            #la puntuación que lleva el jugador
            self.score = 0

        else: #análogo al anterior jugador
            pg.sprite.Sprite.__init__(self)
            self.image = pg.image.load(st.persona2).convert()
            self.rect = self.image.get_rect()
            self.rect.center = st.inicio2
            self.image.set_colorkey(st.BLACK)
            self.pos = vec(st.inicio2[0], st.inicio2[1])
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            self.score = 0


    #esta función va a servir para mover al jugador
    def update(self):
        self.acc = vec(0,0)
        keys = pg.key.get_pressed()
        
        #según que tecla se pulse, se realiza una cosa
        if keys[pg.K_LEFT]:
            self.acc.x += -st.player_acc
        elif keys[pg.K_RIGHT]:
            self.acc.x += st.player_acc
        elif keys[pg.K_DOWN]:
            self.acc.y += st.player_acc
        elif keys[pg.K_UP]:
            self.acc.y += -st.player_acc
        
        #mueve al jugador
        self.acc += self.vel * st.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        
        #posiciona al jugador
        self.rect.center = self.pos
        
        
#Definimos la clase para el camino del fondo
class Path(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        #importa la imagen
        self.image = pg.image.load(st.path).convert()
        
        #crea el rectangulo y lo posiciona
        self.rect = self.image.get_rect()
        self.rect.center = (st.WIDTH /2, st.HEIGHT / 2)
        
#Definimos la clase para las paredes
class Pared(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        
        #crea un rectangulo de grosor w y altura h
        self.image = pg.Surface((w,h))
        
        #pinta el rectángulo de azul
        self.image.fill(st.BLUE)
        
        #crea su rectángulo
        self.rect = self.image.get_rect()
        
        #lo posiciona en la posición (x,y)
        self.rect.x = x
        self.rect.y = y
        
#Definimos la clase para las banderas
class Flags(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        
        #importa la imagen
        self.image = pg.image.load(st.bandera_roja).convert()
        
        #crea el rectangulo y lo posiciona
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        #esto sirve para que se defina la silueta bien
        self.image.set_colorkey(st.BLACK)
        
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.35', 5001))
    print('connected')
    game = Game()
    auxside = s.recv(1204)
    side=int(auxside)
    print(f"I am playing player {side}")
    #gameinfo=s.recv(1024).decode()
    #gameinfo=json.loads(gameinfo)
    #game.update(gameinfo)
    display = Display(game)
    while game.is_running():
        events = display.analyze_events(side)
        for ev in events:
            s.send(ev)
            if ev == 'quit':
                game.stop()
            s.send("next")
            gameinfo = s.recv()
            game.update(gameinfo)
            display.refresh()
            display.tick()
            


if __name__=="__main__":
    main()
