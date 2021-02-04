##
## EPITECH PROJECT, 2020
## 
## File description:
## 
##

import neuralnetwork as nn

class NeuroEvolution:
    net_count = 0
    networks = []

    def __init__(self, network, amnt):
        self.net_count = amnt
        self.generate(network, amnt)
        self.networks = []
        for i in range(0, amnt):
            self.networks.append(network.new())
            self.networks[i].network_id = i
        
    def generate(self, network, amnt):
        self.networks = []
        for i in range(0, amnt):
            self.networks.append(network.copy())
            self.networks[i].network_id = i

    def regenerate(self, index, mutate_rate, learning_rate, amnt):
        for i in range(0, len(self.networks)):
            if i is not index:
                self.networks[i].destroy()
        self.generate(self.networks[index], amnt)
        self.mutateAll(mutate_rate, learning_rate)

    def regenerateFromNetwork(self, network, learning_rate, amnt):
        self.generate(network, amnt)
        self.tweakAll(learning_rate)

    def tweakAll(self, learning_rate):
        for i in range(1, self.net_count):
            self.networks[i].tweakWeights(learning_rate)

    def mutateAll(self, mutate_rate, learning_rate):
        for i in range(1, self.net_count):
            self.networks[i].mutate(mutate_rate, learning_rate)