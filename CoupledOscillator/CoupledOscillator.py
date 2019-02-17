from __future__ import print_function
import numpy as np
import time

"""
init:
    state = 0
    c = random(0,T)
step:
    if(a neighbor flashed)
        c = c + k * c
    else
        c = c + 1
    if(c >= T)
        state = 1
        c = 0
    else
        state = 0
"""

class Oscillator(object):
    def __init__(self, T=100, k=0.5):
        self.state = 0
        self.c = np.random.randint(0,T)
        self.T = T
        self.k = k
        # self.trigger = False
    
    def step(self, is_neighbour_triggered):
        if is_neighbour_triggered:
            # print('triggered')
            self.c = self.c + self.k*self.c 
        else:
            self.c = self.c + 1

        if (self.c >= self.T):
            # if self.state==0:
            #     self.state = 1
            # else:
            #     self.state = 0
            self.state = 1
            self.c=0
            # self.trigger = True
        else:
            self.state=0

    def is_triggered(self):
        # if self.trigger:
        #     self.trigger = False
        #     return True
        # else:
        #     return False
        return self.c==0


class CoupledOscillator(object):

    def __init__(self, grid=(10,10),T=100):
        self.width = grid[0]
        self.height = grid[1]
        self.grid = np.zeros(grid)
        self.plot_now = True
        self.initialize()

    def initialize(self):
        self.array = [[None for i in range(self.width)] for j in range(self.height) ]
        for i in range(self.width):
            for j in range(self.height):
                self.array[i][j] = Oscillator()

    def step_all(self):
        for i in range(self.width):
            for j in range(self.height):
                trigger = self.check_neighbours_trigger(i, j)
                self.array[i][j].step(trigger)
                # self.plot_now = trigger

    def check_neighbours_trigger(self,i,j):
        neighbours = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        for neighbour in neighbours:
            _i,_j = neighbour
            if (_i>=0 and _i<self.width) and (_j>=0 and _j<self.height):
                if self.array[_i][_j].is_triggered():
                    return True
        return False

    def run(self):
        for i in range(50000):
            self.step_all()
            if self.plot_now:
                self.plot()
            time.sleep(0.5)            


    def plot(self):
        for i in range(self.width):
            for j in range(self.height):
                self.grid[i,j] = self.array[i][j].state
        print('-'*80)
        print(self.grid,'\r' )


if __name__ == '__main__':
    co = CoupledOscillator()
    co.run()