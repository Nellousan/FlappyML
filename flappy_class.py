##
## EPITECH PROJECT, 2020
##
## File description:
##
##

import pygame as pg
import numpy as np

class vect():
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


class player():
    pos = None
    speed = None
    size = None
    alive = True
    score = 0
    color = None

    def __init__(self, pos, size=vect(32, 32)):
        self.pos = pos
        self.speed = vect(0, 0)
        self.size = size
        self.alive = True
        self.score = 0
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))


    def destroy(self):
        del self.pos
        del self.speed
        del self

class obstacle():
    pos = None
    size = None
    to_destroy = False

    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def destroy(self):
        del self.pos
        del self.size
        del self

class game():
    p_count = 0
    players = None
    gravity = 0
    player_radius = 0
    rising_speed = 0
    scroller_speed = 0
    clock = None
    screen = None
    width = 0
    height = 0
    obstacle = []
    o_timer = 0
    wait_time = 0
    diff_growth = 0

    def __init__(self, p_count, gravity, rising_speed, player_radius=15, scroller_speed=150, wait_time=2000, diff_growth=5):
        self.clock = pg.time.Clock()
        self.o_clock = pg.time.Clock()
        self.gravity = gravity
        self.rising_speed = rising_speed
        self.scroller_speed = scroller_speed
        self.wait_time = wait_time
        self.diff_growth = diff_growth
        self.screen = pg.Surface((800, 600))
        self.width, self.height = self.screen.get_size()
        self.p_count = p_count
        self.initPlayers(p_count)
        self.player_radius = player_radius

    def initPlayers(self, p_count):
        self.players = []
        for i in range(0, p_count):
            self.players.append(player(vect(150, 250)))


    def playersDelAll(self):
        for i in range(0, len(self.players)):
            self.players[i].destroy()

    def playersReset(self):
        p_count = len(self.players)
        self.playersDelAll()
        self.initPlayers(p_count)

    def gameReset(self):
        self.playersReset()
        self.obstacle = []
        self.clock.tick()

    def updatePlayer(self, player, i):
        if player.pos.y < 0 or player.pos.y > self.height:
            player.alive = False
            return
        prect = pg.Rect(player.pos.x, self.screen.get_size()[1] - player.pos.y, player.size.x, player.size.y)
        for i in range(0, len(self.obstacle)):
            orect = pg.Rect(self.obstacle[i].pos.x, self.obstacle[i].pos.y, self.obstacle[i].size.x, self.obstacle[i].size.y)
            if prect.colliderect(orect) == 1:
                player.alive = False
                return
        player.speed.y -= self.gravity * self.clock.get_time() / 1000
        player.pos.y += player.speed.y * self.clock.get_time() / 1000
        player.score += 1

    def updateObstacle(self, obstacle, i):
        if obstacle.pos.x < 0 - obstacle.size.x:
            obstacle.to_destroy = True
            return
        obstacle.pos.x -= self.scroller_speed * self.clock.get_time() / 1000


    def update(self):
        self.clock.tick()
        for i in range(0, len(self.players)):
            if self.players[i].alive is True:
                self.updatePlayer(self.players[i], i)
        for i in range(0, len(self.obstacle)):
            self.updateObstacle(self.obstacle[i], i)
        for i in range(0, len(self.obstacle)):
            if self.obstacle[i].to_destroy is True:
                self.obstacle[i].destroy()
                self.obstacle.pop(i)
                break
        if pg.time.get_ticks() - self.o_timer > self.wait_time:
            self.o_timer = pg.time.get_ticks()
            self.createObstacle()

    def playerPlay(self, index=0):
        self.players[index].speed.y = self.rising_speed

    def createObstacle(self):
        posy = np.random.random_integers(self.height - 100)
        self.obstacle.append(obstacle(vect(self.width, posy), vect(100, 100)))

    def isOver(self):
        for i in range(0, self.p_count):
            if self.players[i].alive is True:
                return False
        return True

    def getData(self, index):
        ret = None
        ret2 = None
        ret3 = None
        if len(self.obstacle) is 0:
            ret = pg.Vector2(0, 0)
            ret2 = pg.Vector2(0, 0)
        elif len(self.obstacle) is 1:
            ret = self.obstacle[0].pos
            ret2 = self.obstacle[0].size
        elif len(self.obstacle) > 1:
            if self.obstacle[0].pos.x + self.obstacle[0].size.x < self.players[index].pos.x:
                ret = self.obstacle[1].pos
                ret2 = self.obstacle[1].size
            else:
                ret = self.obstacle[0].pos
                ret2 = self.obstacle[0].size

    #   if len(self.obstacle) is 0:
    #        ret = pg.Vector2(0, 0)
    #        ret2 = pg.Vector2(0, 0)
    #        ret3 = pg.Vector2(0, 0)
    #    elif len(self.obstacle) is 1:
    #        ret = self.obstacle[0].pos
    #        ret2 = pg.Vector2(0, 0)
    #        ret3 = pg.Vector2(0, 0)
    #    elif len(self.obstacle) is 2:
    #        ret = self.obstacle[0].pos
    #        ret2 = self.obstacle[1].pos
    #        ret3 = pg.Vector2(0, 0)
    #    else:
    #        ret = self.obstacle[0].pos
    #        ret2 = self.obstacle[1].pos
    #        ret3 = self.obstacle[2].pos        
        mat = np.zeros((4, 1))
        mat[0][0] = self.players[index].pos.y / self.height
        mat[1][0] = ret.y / self.height
        mat[2][0] = ret.x /self.width
        mat[3][0] = (ret.y + ret2.y) / self.height
    #    mat[4][0] = (ret.x + ret2.x) / self.width
        
        return mat
    
    def getFirstAlive(self):
        for i in range(0, len(self.players)):
            if self.players[i].alive is True:
                return i
        return 0

    def getBest(self):
        ret = 0
        netid = 0
        for i in range(0, len(self.players)):
            if self.players[i].score > ret:
                ret = self.players[i].score
                netid = i
        return netid

    def getPlayerAliveCount(self):
        res = 0
        for i in range(0, len(self.players)):
            res = res + 1 if self.players[i].alive is True else res
        return res