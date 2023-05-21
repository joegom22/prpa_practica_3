#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 20:49:47 2023

@author: prpa
"""


from multiprocessing.connection import Listener, Client
from multiprocessing import Process, Manager, Value, Lock
import traceback, sys, os, json
import settings as st
import pygame as pg
import time

class Player():
    def __init__(self, n_player):
        """
        Función de la clase Player que inicializa un player con número de jugador dado y posición vacía.
        
        args
            self
            n_player: int --> número de jugador
        """
        self.n_player = n_player
        self.pos = [None, None]

    def get_pos(self):
        """
        Función de la clase Player que devuelve la posición del jugador
        
        args
            self
        """
        return self.pos

    def get_n_player(self):
        """
        Función de la clase Player que devuelve el número de jugador
        
        args
            self
        """
        return self.n_player

    def set_pos(self, pos):
        """
        Función de la clase Player que cambia la posición del jugador por una dada
        
        args
            self
            pos: [int, int] --> nueva posición
        """
        self.pos = pos

    def __str__(self):
        """
        Función de la clase Player que permite visualizar por pantalla el estado del jugador
        
        args
            self
        """
        return f"P<{self.n_player, self.pos}>"
    
class Flag():
    def __init__(self):
        """
        Función de la clase Flag que inicializa una bandera con posición vacía
        
        args
            self
        """
        self.pos=[ None, None ]

    def get_pos(self):
        """
        Función de la clase Flag que devuelve la posición de la bandera
        
        args
            self
        """
        return self.pos

    def set_pos(self, pos):
        """
        Función de la clase Flag que cambia la posición de la bandera por una dada
        
        args
            self
            pos: [int, int] --> nueva posición
        """
        self.pos = pos

    def __str__(self):
        """
        Función de la clase Flag que permite visualizar por pantalla el estado de la bandera
        
        args
            self
        """
        return f"F<{self.pos}>"

class Wall():
    def __init__(self):
        """
        Función de la clase Wall que inicializa un muro con posición y medidas vacías
        
        args
            self
        """
        self.pos = [None, None]
        self.measures = [None, None]

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

    def set_pos(self, pos):
        """
        Función de la clase Wall que cambia la posición del muro por una dada
        
        args
            self
            pos: [int, int] --> nueva posición
        """
        self.pos = pos
        
    def set_measures(self, meas):
        """
        Función de la clase Wall que cambia las medidas del muro por unas dadas
        
        args
            self
            meas: [int, int] --> nuevas medidas
        """
        self.measures=meas    

    def __str__(self):
        """
        Función de la clase Wall que permite visualizar por pantalla el estado del muro
        
        args
            self
        """
        return f"W<{self.pos}>"
    
class Game():
    def __init__(self):
        """
        Función de la clase Game que inicializa un juego con sus jugadores, banderas, bandera visible, muros, puntuación y valor de jugando o no todos vacíos
        
        args
            self
        """
        self.players = [Player(0), Player(1)]
        self.flags = [ Flag() for i in range(len(st.banderas)) ]
        self.flagsvisible = [Flag()]
        self.walls = [Wall() for i in range(len(st.paredes)) ]
        self.score = [0,0]
        self.running = True
        
    def get_player(self, n_player):
        """
        Función de la clase Game que dado un número de jugador devuelve el jugador con dicho número
        
        args
            self
            n_player: int --> número de jugador
        """
        return self.players[n_player]

    def set_pos_player(self, n_player, pos):
        """
        Función de la clase Game que dado un número de jugador y una posición cambia la posición del jugador con dicho número a la posición dada
                
        args
            self
            n_player: int --> número de jugador
            pos: [int, int] --> nueva posición
        """
        self.players[n_player].set_pos(pos)
        
    def set_walls(self, info):
        """
        Función de la clase Game que dada la información sobre unos muros establece como muros del juego dichos muros
                
        args
            self
            info: [[[int, int], [int, int]]] --> posiciones y medidas
        """
        j=0
        for i in info:
            self.walls[j].set_pos(i[0])
            self.walls[j].set_measures(i[1]) 
            j+=1
            
    def get_flag(self):
        """
        Función de la clase Game que devuelve la bandera visible
                
        args
            self
        """
        return self.flagsvisible[0]
    
    def set_flag_pos(self, info):
        """
        Función de la clase Game que dada la información sobre unas banderas establece como banderas del juego dichas banderas
                
        args
            self
            info: [[int, int]] --> posiciones
        """
        j = 0
        for i in info:
            self.flags[j].set_pos(i)
            j += 1

    def get_score(self):
        """
        Función de la clase Game que devuelve la puntuación
        
        args
            self
        """
        return self.score

    def set_score(self, score):
        """
        Función de la clase Game que cambia la puntuación por una dada
        
        args
            self
            score: [int, int] --> nueva puntuación
        """
        self.score = score
        
    def update(self, gameinfo):
        """
        Función de la clase Game que llama a las funciones apropiadas para actualizar toda la información del juego por una nueva dada
        
        args
            self
            gameinfo: Dict --> Nueva información
        """
        self.set_pos_player(0, gameinfo['pos_player_0'])
        self.set_pos_player(1, gameinfo['pos_player_1'])
        self.set_walls(gameinfo['walls'])
        self.set_flag_pos(gameinfo['pos_flag'])
        self.set_score(gameinfo['score'])
        self.running = gameinfo['is_running']

    def is_running(self):
        """
        Función de la clase Game que devuelve si el juego está corriendo o no
        
        args
            self
        """
        return self.running

    def stop(self):
        """
        Función de la clase Game que cambia el valor de si le juego está corriendo a falso
        
        args
            self
        """
        self.running = False

    def __str__(self):
        """
        Función de la clase Game que nos permite visualizar por pantalla el estado de los dos jugadores del juego
        
        args
            self
        """
        return f"G<{self.players[0]}:{self.players[1]}>"
    
class PlayerSprite(pg.sprite.Sprite):
    def __init__(self, player):
        """
        Función de la clase PlayerSprite que dado un jugador inicializa el sprite del jugador en su posición a una imagen concreta en función de su número
        
        args
            self
            player: Player --> Jugador
        """
        self.player=player
        self.n_player=player.n_player
        super().__init__()
        if self.n_player == 1:
            self.image = pg.image.load(st.persona1).convert() #cargamos su imagen (la imagen del 'alien')
        else:
            self.image = pg.image.load(st.persona2).convert() #cargamos su imagen 

        self.rect = self.image.get_rect() #creamos un rectángulo a su alrededor
        self.rect.center = self.player.get_pos()
        self.image.set_colorkey(st.BLACK)
        self.pos = self.player.get_pos()
        self.vel = [0,0]
        self.acc = [0,0]
        self.score = 0
    
    def update(self):
        """
        Función de la clase PlayerSprite que actualiza la posición del sprite a la posición del jugador
        
        args
            self
        """
        pos = self.player.get_pos()
        self.rect.centerx, self.rect.centery = pos

    def __str__(self):
        """
        Función de la clase PlayerSprite que permite visualizar por pantalla el estado del jugador del sprite
        
        args
            self
        """
        return f"S<{self.player}>"   

class FlagSprite(pg.sprite.Sprite):
    def __init__(self, flag):
        """
        Función de la clase FlagSprite que dada una bandera inicializa el sprite de la bandera en su posición a una imagen concreta
        
        args
            self
            flag: Flag --> Bandera
        """
        super().__init__()
        self.flag=flag
        self.image = pg.image.load(st.bandera_roja).convert()
        
         #crea el rectangulo y lo posiciona
        self.rect = self.image.get_rect()
        self.rect.x = self.flag.get_pos()[0]
        self.rect.y = self.flag.get_pos()[1]
        
        self.image.set_colorkey(st.BLACK) #esto sirve para que se defina la silueta bien
    
    def get_pos(self):
        """
        Función de la clase FlagSprite que devuelve la posición de la bandera del sprite
        
        args
            self
        """
        return self.flag.get_pos()
        
    def update(self):
        """
        Función de la clase FlagSprite que cambia la posición del sprite por la posición de la bandera asociada
        
        args
            self
        """
        pos = self.flag.get_pos()
        self.rect.centerx, self.rect.centery = pos
    
class WallSprite(pg.sprite.Sprite):
    def __init__(self, wall):
        """
        Función de la clase WallSprite que dado un muro inicializa el sprite del muro en su posición a un rectángulo de iguales dimensiones que las del muro
        
        args
            self
            wall: Wall --> Muro
        """
        self.wall = wall
        super().__init__()
        self.image = pg.Surface((self.wall.get_measures())) #crea un rectangulo de grosor w y altura h
        self.image.fill(st.BLUE) #pinta el rectángulo de azul
        self.rect = self.image.get_rect() #crea su rectángulo
        
        #lo posiciona en la posición (x,y)
        self.rect.x = self.wall.get_pos()[0]
        self.rect.y = self.wall.get_pos()[1]
         
class Display():
    def __init__(self, game):
        """
        Función de la clase Display que dado un juego incializa lo que se muestra por pantalla con la información que recibe del juego
        
        args
            self
            game: Game --> juego del que recibe la información
        """
        pg.init()
        self.screen = pg.display.set_mode(st.SIZE)
        self.clock =  pg.time.Clock()  #FPS
        self.background = pg.image.load(st.path).convert()
        self.screen.blit(self.background, (0, 0))
        self.game=game
        self.playersprites=[PlayerSprite(self.game.get_player(0)), PlayerSprite(self.game.get_player(1))]
        #self.flag=FlagSprite(self.game.get_flag())
        self.wall=[]
        for i in self.game.walls:
            print(i.get_pos())
            self.wall.append(WallSprite(i))
            
        self.flags2 = []
        for i in self.game.flags:
            print(i.get_pos())
            self.flags2.append(FlagSprite(i))
            
        self.flag_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        for flag in self.flags2:
            self.all_sprites.add(flag)
            self.flag_sprites.add(flag) 
            
        self.players_group = pg.sprite.Group()
        self.wall_sprites = pg.sprite.Group()
        for player  in self.playersprites:
            self.all_sprites.add(player)
            self.players_group.add(player)
        #self.all_sprites.add(self.flag)
        #self.flag_sprites.add(self.flag)
        
        for walls in self.wall:
            self.all_sprites.add(walls)
            self.wall_sprites.add(walls)
        pg.display.flip()
    
    def analyze_events(self, n_player):
        """
        Función de la clase Display que dado un número de jugador analiza y devuelve los eventos que ocurren para ese jugador
        
        args
            self
            n_player: int --> número de jugador
        """
        events = []
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    events.append("quit")
                elif event.key == pg.K_UP:
                    events.append("up")
                elif event.key == pg.K_DOWN:
                    events.append("down")
                elif event.key == pg.K_RIGHT:
                    events.append("right")
                elif event.key == pg.K_LEFT:
                    events.append("left")
            elif event.type == pg.QUIT:
                events.append("quit")
            elif pg.sprite.spritecollide(self.playersprites[n_player], self.flag_sprites, False):      
                flag_collision = pg.sprite.spritecollide(self.playersprites[n_player], self.flag_sprites, False)[0]  
                flag_collision_getpos = flag_collision.get_pos()
                events.append(("flag",flag_collision_getpos))

            elif pg.sprite.spritecollide(self.playersprites[n_player], self.wall_sprites, False):
                events.append("wall")
        return events  

    def refresh(self):
        """
        Función de la clase Display que vuelve a cargar la pantalla de visualización
        
        args
            self
        """
        #self.flag_sprites = pg.sprite.Group()
        #for i in self.flag_sprites:
        #    self.flag = FlagSprite(i)
        #    self.all_sprites.add(self.flag)
        #    self.flag_sprites.add(self.flag)    
        #self.flag_sprites.update()
        self.all_sprites.update()
        self.screen.blit(self.background, (0, 0))
        score = self.game.get_score()
        font = pg.font.Font(None, 74)
        text = font.render(f"{score[0]}", 1, st.BLACK)
        self.screen.blit(text, (250, 10))
        text = font.render(f"{score[1]}", 1, st.BLACK)
        self.screen.blit(text, (500, 10))
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        
    def display_end(self):
        """
        Función de la clase Display que muestra la pantalla de final de juego acorde al jugador ganador
        
        args
            self
        """
        score = self.game.get_score()
        if score[0] == 3:
            self.screen = pg.display.set_mode([1000,650])
            self.background = pg.image.load(st.fin_p0).convert()
            self.screen.blit(self.background, (0, 0))
            pg.display.flip()
        else:
            self.screen = pg.display.set_mode([1000,650])
            self.background = pg.image.load(st.fin_p1).convert()
            self.screen.blit(self.background, (0, 0))
            pg.display.flip()
            
    def tick(self):
        """
        Función de la clase Display para actualizar el reloj
        
        args
            self
        """
        self.clock.tick(st.FPS)

    @staticmethod
    def quit():
        """
        Función sin argumentos de la clase Display que sale del juego
        """
        pg.quit()
        
def main():
    """
    Función principal que se ejecuta al ejecutar el programa.
    Se conecta a la sala y recibe la información del juego, va enviando los eventos a la sala para que esta los ejecute y va actualizando la información con lo que la sala le manda
    """
    try:
        with Client(("10.0.2.15", 5000), authkey=b'secret password') as conn:
            game = Game()
            n = conn.recv()
            print(f"I am playing {n}")
            gameinfo = conn.recv()
            game.update(gameinfo)
            display = Display(game)
            while game.is_running():
                events = display.analyze_events(n)
                for ev in events:
                    conn.send(ev)
                    if ev == 'quit':
                        game.stop()
                conn.send("next")
                gameinfo = conn.recv()
                game.update(gameinfo)
                display.refresh()
                display.tick()
            display.display_end()
            time.sleep(10)
            print("fin")
    except:
        traceback.print_exc()
    finally:
        pass
        #pg.quit()

if __name__=="__main__":
    main()