##
## EPITECH PROJECT, 2020
##
## File description:
##
##

import pygame as pg
import numpy as np
import math

def sig(x):
    return 1 / (1 + np.exp(-round(x, 6)))

class NeuralNetwork:
    input_amnt = 0
    network_id = None
    layers_param = None
    layers = []
    res = []
    last_inputs = []
    f = None

    def __init__(self, network_id, input_amnt, layers, activation_function=sig):
        self.network_id = network_id
        self.input_amnt = input_amnt
        self.layers_param = layers
        self.layers = [[[]]] * len(layers)
        self.layers[0] = np.random.ranf((layers[0], input_amnt + 1)) * 10 - 5
        self.f = activation_function
        for i in range(1, len(layers)):
            self.layers[i] = np.random.ranf((layers[i], layers[i - 1] + 1)) * 10 - 5
        return

    def feedForward(self, inputs):
        self.res = [[[]]] * len(self.layers)
        inputs = np.append(inputs, 1.)
        inputs = np.reshape(inputs, (len(inputs), -1))
        self.last_inputs = inputs.copy()
        self.res[0] = self.layers[0].dot(inputs)
        for j in range(0, len(self.layers[0])):
                self.res[0][j][0] = self.f(self.res[0][j][0])
        for i in range(1, len(self.layers)):
            self.res[i - 1] = np.append(self.res[i - 1], 1)
            self.res[i - 1] = np.reshape(self.res[i - 1], (len(self.res[i - 1]), -1))
            self.res[i] = self.layers[i].dot(self.res[i - 1])
            for j in range(0, len(self.res[i])):
                self.res[i][j][0] = self.f(self.res[i][j][0])
        return self.res[len(self.layers) - 1]

    def tweakWeights(self, rate):
        for i in range(0, len(self.layers)):
            for j in range(0, len(self.layers[i])):
                for k in range(0, len(self.layers[i][j])):
                    self.layers[i][j][k] += (np.random.ranf() * 2 - 1) * rate
        return

    def mutate(self, mutate_rate, learning_rate):
        for i in range(0, len(self.layers)):
            for j in range(0, len(self.layers[i])):
                for k in range(0, len(self.layers[i][j])):
                    if np.random.ranf() < mutate_rate:
                        self.layers[i][j][k] += (np.random.ranf() * 2 - 1) * learning_rate
        return

    def destroy(self):
         del self

    def copy(self):
        ret = NeuralNetwork(self.network_id, self.input_amnt, (1, 1))
        ret.layers = self.layers.copy()
        for i in range(0, len(ret.layers)):
            ret.layers[i] = self.layers[i].copy()
        return ret

    def new(self):
        return NeuralNetwork(0, self.input_amnt, self.layers_param)


class Visualizer:
    screen = None
    font = None
    size = None

    def __init__(self, size,font="consolas.ttf", font_size=30):
        self.size = size
        self.screen = pg.Surface(size)
        self.font = pg.font.SysFont(font, font_size)

    def drawText(self, string, pos, color=(255, 255, 255)):
        text = self.font.render(string, False, color)
        self.screen.blit(text, pos)

    def drawNetwork(self, network, s=1):
        self.screen.fill((30, 30, 40))
        res = network.res
        lay = network.layers
        ins = network.last_inputs
        lc = len(network.res)
        yoff = 100
        xoff = 100
        yofff = 0
        for i in range(0, len(res)):
            if len(res[i]) > yofff:
                yofff = len(res[i]) if i is len(res[i]) else len(res[i]) - 1
        yofff = len(ins) + 1 if len(ins) + 1 > yofff else yofff

        for i in range(0, len(ins)):
            text = self.font.render(str(ins[i][0]), False, (220, 220, 220))
            yoffff = int((yofff - len(ins)) * 40 / 2)
            rect = pg.Rect(int(self.size.x) - xoff, i * 40 + yoff + yoffff - 10, 20, 20)
            color = (220, 220, 220) if i is not len(ins) - 1 else (0, 0, 255)
            pg.draw.rect(self.screen, color, rect)
            self.screen.blit(text, (rect.left + 30, rect.top))
        for j in range(0, len(lay[0])):
            yoffff = int((yofff - len(lay[0]) - 1) * 40 / 2)
            yoffff2 = int((yofff - len(ins)) * 40 / 2)
            for k in range(0, len(ins)):
                cvar = sig(network.layers[0][j][k])
                color = (255 * (1 - cvar), 255 * cvar, 0)
                pos1 = int(self.size.x) - (80 + xoff), j * 40 + yoff + yoffff
                pos2 = int(self.size.x) - (xoff), k * 40 + yoff + yoffff2
                pg.draw.line(self.screen, color, pos1, pos2)
        
    
        for i in range(1, len(lay)):
            yoffff = int((yofff - len(res[i])) * 40 / 2)
            yoffff2 = int((yofff - len(res[i - 1])) * 40 / 2)
            for j in range(0, len(lay[i])):
                for k in range(0, len(lay[i - 1]) + 1):
                    cvar = sig(network.layers[i][j][k])
                    color = (255 * (1 - cvar), 255 * cvar, 0)
                    pos1 = int(self.size.x) - ((i + 1) * 80 + xoff), j * 40 + yoff + yoffff
                    pos2 = int(self.size.x) - ((i) * 80 + xoff), k * 40 + yoff + yoffff2
                    pg.draw.line(self.screen, color, pos1, pos2)
        for i in range(0, len(res)):
            yoffff = int((yofff - len(res[i])) * 40 / 2)
            for j in range(0, len(res[i])):
                if i is not len(res) - 1 and j is len(res[i]) - 1:
                    color = (0, 0, 200)
                else:
                    color = (255 * res[i][j], 255 * res[i][j], 255 * res[i][j])
                pg.draw.circle(self.screen, color, (int(self.size.x) - ((i + 1) * 80 + xoff), j * 40 + yoff + yoffff), 10)

class Console:
    screen = None
    font = None
    font_size = None
    size = None
    logs = None
    color_logs = None

    def __init__(self, size,font="consolas.ttf", font_size=30):
        self.size = size
        self.screen = pg.Surface(size)
        self.font = pg.font.SysFont(font, font_size)
        self.font_size = font_size
        self.logs = []
        self.color_logs = []

    def drawLog(self):
        self.screen.fill((40, 30, 30))
        logs = self.logs
        color_logs = self.color_logs
        for i in range(0, len(logs)):
            text = self.font.render(logs[i], False, color_logs[i])
            self.screen.blit(text, (10, self.size.y - (i * self.font_size + (i + 1) * 10) - self.font_size))


    def log(self, string, color=(255, 255, 255)):
        self.logs.insert(0, string)
        self.color_logs.insert(0, color)
        for i in range(0, len(self.logs)):
            if self.size.y - (i * self.font_size + (i + 1) * 10) + self.font_size < 0:
                self.logs.pop(i)
                self.color_logs.pop(i)
                break
        
