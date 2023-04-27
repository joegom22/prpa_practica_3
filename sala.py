from multiprocessing import Manager, Process, Value, Lock
import pygame as pg #importamos el módulo pygame
import settings as st #importamos el archivo con todos los parámetros
import socket
import random
import traceback, sys, os, json

class Player():
    def __init__(self, n_player):
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
        return self.pos
        
    def get_number(self):
        return self.n_player
        
    def moveDown():
        pass
    
    def moveUp():
        pass
    
    def moveLeft():
        pass
    
    def moveRight():
        pass
    
    def __str__(self):
        return f"P<{self.n_player}, {self.pos}>"
        
class Flag():
    def __init__(self, x, y):
        self.pos = [x,y]
    
    def get_pos(self):
        return self.pos
    
    def __str__(self):
        return f"F<{self.pos}>"
        
class Wall():
    def __init__(self, x, y, w, h):
        self.pos = [x,y]
        self.measures = [w, h]
    
    def get_pos(self):
        return self.pos
    
    def get_measures(self):
        return self.measures
        
    def __str__(self):
        return f"W<{self.pos}>"
        

class Game():
    def __init__(self, manager):
        self.players = manager.list( [Player(0), Player(1)] )
        lista = []
        for i in st.banderas:
            lista.append(Flag(i[0],i[1]))
        self.flags = manager.list(lista)
        lista2 = []
        for i in st.paredes:
            lista2.append(Wall(i[0],i[1],i[2],i[3]))
        self.walls = manager.list(lista2)
        self.flagsvisible = manager.list() 
        self.score = manager.list([0,0])
        self.running = Value('i', 1)# 1 running
        self.lock = Lock()
        self.add_flag(manager)
    
    def get_player(self, n_player):
        return self.players[n_player]
    
    def get_flag(self):
        return self.flagsvisible[0]
    
    def get_score(self):
        return list(self.score) 

    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.running.value = 0 
        
    def moveUp(self, n_player):
        p = self.players[n_player]
        p.moveUp()
        self.players[n_player]=p
        
    def moveDown(self, n_player):
        p = self.players[n_player]
        p.moveDown()
        self.players[n_player]=p
        
    def moveLeft(self, n_player):
        p = self.players[n_player]
        p.moveLeft()
        self.players[n_player]=p
        
    def moveRight(self, n_player):
        p = self.players[n_player]
        p.moveRight()
        self.players[n_player]=p

   
    def add_flag(self,manager):
        flag = random.choice(self.flags)
        self.flagsvisible.append(flag)
        #self.all_sprites.add()
        
            
    def win_flag(self, n_player):
        self.lock.acquire()
        collision = pg.sprite.spritecollide(self.players[n_player], self.flagsvisible, False)
        if collision:
            collision[0].kill()
            self.add_flag()
            self.players[n_player].score += 1
            self.score[n_player] += 1
            self.players[0].pos = [st.inicio1[0],st.inicio1[1]]
            self.players[1].pos = [st.inicio2[0],st.inicio2[1]]
        if self.players[n_player].score == 3:
            self.running.Value = 0
        self.lock.release()
        
    def collide_wall(self, n_player):
        collision = pg.sprite.spritecollide(self.players[n_player], self.walls, False)
        if collision:
            if n_player == 0:
                self.players[n_player].pos = [st.inicio1[0],st.inicio1[1]]
            else:
                self.players[n_player].pos = [st.inicio2[0],st.inicio2[1]]      
        
            
    def get_info(self):
        info = {
            "pos_player_0": self.players[0].get_pos(),
            "pos_player_1": self.players[1].get_pos(),
            "pos_flag": self.flagsvisible[0].get_pos(),
            "score": list(self.score),
            "is_running": self.running.value == 1}
        return info
    
    def __str__(self):
        return f"G<{self.players[0]}:{self.players[1]}:{self.running.value}>"
    
def player(n_player, conn, game):
    try:
        print(f"starting player {n_player}")
        gameinfo = game.get_info()
        conn.send(json.dumps(gameinfo).encode())
        while game.is_running():
            command = ""
            while command != "next":
                command = conn.recv(1024)
                if command == "up":
                    game.moveUp(n_player)
                elif command == "down":
                    game.moveDown(n_player)
                elif command == "left":
                    game.moveLeft(n_player)
                elif command == "right":
                    game.moveRight(n_player)
                elif command == "flag":
                    game.win_flag(n_player)
                elif command == "quit":
                    game.stop()
            gameinfo = game.get_info()
            conn.send(json.dumps(gameinfo).encode())
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {game}")   

def main():
    n=0
    manager = Manager()
    host = '0.0.0.0'
    port = 5000
    mysocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind((host,port))
    while n<2:
	    mysocket.listen(10)
	    print('Listening')
	    game = Game(manager)
	    conn, addr= mysocket.accept()
	    print('accepted')
	    n += 1
	    if n ==1:
		    n_player = 0
		    players = [None, None]
		    #gameinfo=game.get_info()
		    conn.send(str(n_player).encode())
		    #conn.send(json.dumps(gameinfo).encode())
		    players[n_player] = Process(target=player, args=(n_player, conn, game))
	    else:
	        n_player = 1
	        conn.send(str(n_player).encode())
	        #gameinfo=game.get_info()
	        #conn.send(json.dumps(gameinfo).encode())
	        players[n_player] = Process(target=player, args=(n_player, conn, game))
	        players[0].start()
	        players[1].start()
	        n_player = 0
	        players = [None, None]
	        game = Game(manager)
	        
if __name__=='__main__':
    main()     
