from multiprocessing.connection import Listener, Client
from multiprocessing import Process, Manager, Value, Lock
import traceback, sys, os, json
import socket
import settings as st
import pygame as pg

class Player():
    def __init__(self, n_player):
        self.n_player = n_player
        self.pos = [None, None]

    def get_pos(self):
        return self.pos

    def get_n_player(self):
        return self.n_player

    def set_pos(self, pos):
        self.pos = pos

    def __str__(self):
        return f"P<{self.n_player, self.pos}>"
    
class Flag():
    def __init__(self):
        self.pos=[ None, None ]

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def __str__(self):
        return f"F<{self.pos}>"

class Wall():
    def __init__(self):
        self.pos = [None, None]
        self.measures = [None, None]

    def get_pos(self):
        return self.pos
    
    def get_measures(self):
        return self.measures

    def set_pos(self, pos):
        self.pos = pos
        
    def set_measures(self, meas):
        self.measures=meas    

    def __str__(self):
        return f"W<{self.pos}>"
    
class Game():
    def __init__(self):
        self.players = [Player(0), Player(1)]
        self.flags = [ Flag() for i in range(len(st.banderas)) ]
        self.flagsvisible = [Flag()]
        self.walls = [Wall() for i in range(len(st.paredes)) ]
        self.score = [0,0]
        self.running = True
        
    def get_player(self, n_player):
        return self.players[n_player]

    def set_pos_player(self, n_player, pos):
        self.players[n_player].set_pos(pos)
        
    def set_walls(self, info):
        j=0
        for i in info:
            self.walls[j].set_pos(i[0])
            self.walls[j].set_measures(i[1]) 
            j+=1
            
    def get_flag(self):
        return self.flagsvisible[0]
    
    def set_flag_pos(self, pos):
        self.flagsvisible[0].set_pos(pos)

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score
        
    def update(self, gameinfo):
        self.set_pos_player(0, gameinfo['pos_player_0'])
        self.set_pos_player(1, gameinfo['pos_player_1'])
        self.set_walls(gameinfo['walls'])
        self.set_flag_pos(gameinfo['pos_flag'])
        self.set_score(gameinfo['score'])
        self.running = gameinfo['is_running']

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    def __str__(self):
        return f"G<{self.players[0]}:{self.players[1]}>"
    
class PlayerSprite(pg.sprite.Sprite):
    def __init__(self, player):
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
        pos = self.player.get_pos()
        self.rect.centerx, self.rect.centery = pos

    def __str__(self):
        return f"S<{self.player}>"   

class FlagSprite(pg.sprite.Sprite):
    def __init__(self, flag):
        super().__init__()
        self.flag=flag
        self.image = pg.image.load(st.bandera_roja).convert()
        
         #crea el rectangulo y lo posiciona
        self.rect = self.image.get_rect()
        self.rect.x = self.flag.get_pos()[0]
        self.rect.y = self.flag.get_pos()[1]
        
        self.image.set_colorkey(st.BLACK) #esto sirve para que se defina la silueta bien
        
    def update(self):
        pos = self.flag.get_pos()
        self.rect.centerx, self.rect.centery = pos
    
class WallSprite(pg.sprite.Sprite):
    def __init__(self, wall):
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
        pg.init()
        self.screen = pg.display.set_mode(st.SIZE)
        self.clock =  pg.time.Clock()  #FPS
        self.background = pg.image.load(st.path).convert()
        self.screen.blit(self.background, (0, 0))
        self.game=game
        self.playersprites=[PlayerSprite(self.game.get_player(0)), PlayerSprite(self.game.get_player(1))]
        self.flag=FlagSprite(self.game.get_flag())
        self.wall=[]
        for i in self.game.walls:
            print(i.get_measures())
            self.wall.append(WallSprite(i))
        self.flag_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.players_group = pg.sprite.Group()
        self.wall_sprites = pg.sprite.Group()
        for player  in self.playersprites:
            self.all_sprites.add(player)
            self.players_group.add(player)
        self.all_sprites.add(self.flag)
        self.flag_sprites.add(self.flag)
        for walls in self.wall:
            self.all_sprites.add(walls)
            self.wall_sprites.add(walls)
        pg.display.flip()
    
    def analyze_events(self, n_player):
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
            	events.append("flag")
            	flag_collision = pg.sprite.spritecollide(self.playersprites[n_player], self.flag_sprites, False)[0]
            	flag_collision.kill()
            elif pg.sprite.spritecollide(self.playersprites[n_player], self.wall_sprites, False):
            	events.append("wall")
        return events  

    def refresh(self):
    	self.all_sprites.empty()
    	self.wall_sprites.empty()
    	self.players_group.empty()
    	flag = self.game.get_flag()
    	self.flag = FlagSprite(flag)
    	self.all_sprites.add(self.flag)
    	self.flag_sprites = pg.sprite.Group()
    	self.flag_sprites.add(self.flag)
    	self.flag_sprites.update()
    	self.all_sprites.update()
    	self.screen.blit(self.background, (0, 0))
    	score = self.game.get_score()
    	font = pg.font.Font(None, 74)
    	text = font.render(f"{score[0]}", 1, st.BLACK)
    	self.screen.blit(text, (250, 10))
    	text = font.render(f"{score[1]}", 1, st.BLACK)
    	self.screen.blit(text, (st.SIZE[0]-250, 10))
    	for player in self.playersprites:
    		self.all_sprites.add(player)
    		self.players_group.add(player)
    	for walls in self.wall:
    		self.all_sprites.add(walls)
    		self.wall_sprites.add(walls)
    	self.all_sprites.draw(self.screen)
    	pg.display.flip()
    	"""
    	flag = self.game.get_flag()
    	self.flag = FlagSprite(flag)
    	self.all_sprites.add(self.flag)
    	self.flag_sprites = pg.sprite.Group()
    	self.flag_sprites.add(self.flag)
    	self.flag_sprites.update()
    	self.all_sprites.update()
    	self.screen.blit(self.background, (0, 0))
    	score = self.game.get_score()
    	font = pg.font.Font(None, 74)
    	text = font.render(f"{score[0]}", 1, st.BLACK)
    	self.screen.blit(text, (250, 10))
    	text = font.render(f"{score[1]}", 1, st.BLACK)
    	self.screen.blit(text, (st.SIZE[0]-250, 10))
    	self.all_sprites.draw(self.screen)
    	pg.display.flip()
        """

    def tick(self):
        self.clock.tick(st.FPS)

    @staticmethod
    def quit():
        pg.quit()
        
def main():
    try:
        with Client(("10.9.91.199", 5000), authkey=b'secret password') as conn:
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
    except:
        traceback.print_exc()
    finally:
        pg.quit()

if __name__=="__main__":
    main()
