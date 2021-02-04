##
## EPITECH PROJECT, 2020
## 
## File description:
## 
##

import pygame as pg

def drawObstacle(game, obstacle):
    rect = pg.Rect(obstacle.pos.x, obstacle.pos.y, obstacle.size.x, obstacle.size.y)
    pg.draw.rect(game.screen, (255, 0, 0), rect)

def drawPLayer(game, player):
    rect = pg.Rect(player.pos.x, game.screen.get_size()[1] - player.pos.y, player.size.x, player.size.y)
    pg.draw.rect(game.screen, player.color, rect)

def drawGame(game):
    game.screen.fill((20, 20, 20))
    for i in range(0, len(game.players)):
        if game.players[i].alive is True:
            drawPLayer(game, game.players[i])
    for i in range(0, len(game.obstacle)):
        drawObstacle(game, game.obstacle[i])

def clearGame(game):
    game.screen.fill(0, 0, 0)
