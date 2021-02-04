##
## EPITECH PROJECT, 2020
## 
## File description:
## 
##

import sys
import numpy as np
import pygame as pg
import flappy_class as fpc
import flappy_draw as fpd
import neuralnetwork as nn
import neuroevolution as ne

pg.init()
pg.font.init()
p_count = 200
generation = 0
best_score = 0 
p_best_score = 0
best_gen = 0
mlr = 1
olr = 0.5
lr = olr
mr = 0.1
game = fpc.game(p_count, 1000, 400)
screen = pg.display.set_mode((1400, 900))
visualizer = nn.Visualizer(pg.Vector2(600, 900))
console = nn.Console(pg.Vector2(800, 300))
network = nn.NeuralNetwork(0, 4, (10, 10, 5, 5, 1))
nets = ne.NeuroEvolution(network, p_count)

def updateWindow():
    fpd.drawGame(game)
    screen.blit(game.screen, (0, 0))
    screen.blit(visualizer.screen, (800, 0))
    console.drawLog()
    screen.blit(console.screen, (0, 600))
    pg.display.update()

while True:
    spec = 0
    while game.isOver() is False:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
        game.update()

        for i in range(0, p_count):
            if game.players[i].alive is True:
                data = game.getData(i)
                out = nets.networks[i].feedForward(data)
                if out[0][0] > 0.5:
                    game.playerPlay(i)

        if game.players[spec].alive is False:
            spec = game.getFirstAlive()
        visualizer.drawNetwork(nets.networks[spec])
        visualizer.drawText("Vizualizing net : " + str(spec), pg.Vector2(10, 10))
        visualizer.drawText("Nets alive : " + str(game.getPlayerAliveCount()), pg.Vector2(10, 40))
        visualizer.drawText("Networks per generation : " + str(p_count), pg.Vector2(250, 10))
        visualizer.drawText("Current Score : " + str(game.players[spec].score), pg.Vector2(10, 400), (255, 0, 0))
        visualizer.drawText("Previous Best Score : " + str(p_best_score), pg.Vector2(10, 450), (255, 0, 0))
        visualizer.drawText("Best Score : " + str(best_score), pg.Vector2(10, 500), (255, 0, 0))
        visualizer.drawText("Generation : " + str(generation), pg.Vector2(10, 550), (0, 255, 255))
        visualizer.drawText("Learning Rate : " + str(round(lr, 1)), pg.Vector2(10, 600), (200, 0, 255))        
        visualizer.drawText("Mutate Rate : " + str(round(mr, 1)), pg.Vector2(10, 650), (200, 0, 255))        
        updateWindow()
    
    best = game.getBest()
    p_best_score = game.players[best].score
    if p_best_score > best_score:
#        lr = olr
#        best_gen = generation
        best_score = game.players[best].score
#        best_net = nets.networks[best].copy()
#        console.log("New generation from network : " + str(best), (255, 0, 0))
#    else:
#        lr = lr + 0.1 if lr < mlr else lr
#        console.log("New generation from network : best from gen " + str(best_gen), (255, 0, 0))
    console.log("New generation from network : " + str(best), (255, 0, 0))

    nets.regenerate(best, mr, lr, p_count)

    updateWindow()
    generation += 1
    game.gameReset()
        
