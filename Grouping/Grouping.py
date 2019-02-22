from __future__ import print_function
import numpy as np
import time
import matplotlib.pyplot as plt
import traceback

np.random.seed(41)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)


class Node(object):
    def __init__(self, R=20, P=0.3):
        self.is_initialized = False
        self.is_susceptible = False 
        self.signal = 0
        self.prev_signal = 0
        self.R = R
        self.refractory_timer = R
        self.P = P
        self.counter = 0
    
    def step(self, neighbour_signalled):
        self.prev_signal = self.signal
        if (self.is_susceptible):
            if(neighbour_signalled):
                self.update()
            elif (not self.is_initialized) and (np.random.rand()<self.P):
                self.update()
                self.is_initialized = True
        else:
            self.refractory_timer -= 1
            self.signal = 0
            if (self.refractory_timer <= 0):
                self.is_susceptible = True
        
        if self.prev_signal==self.signal:
            self.counter +=1
        else:
            self.counter = 0
    
    def update(self):
        self.signal = 1
        self.is_susceptible = False
        self.refractory_timer = self.R
    
    def is_triggered(self):
        return self.prev_signal == 1
    
    def is_done(self):
        return self.counter > (1.0/self.P)

class Grid(object):
    def __init__(self, grid_size = (20,20)):
        self.width  = grid_size[0]
        self.height = grid_size[1]
        self.grid = [[Node(P=np.random.rand()) for i in range(self.width)] for j in range(self.height)]
        self.display_grid = np.zeros((self.width,self.height))

        self.four_neighbours = lambda i,j:[        (i,j-1),
                                            (i-1,j),    (i+1,j),    
                                                   (i,j+1)
                                                ]
        self.eight_neighbours = lambda i,j:[(i-1,j-1),(i,j-1),(i+1,j-1),
                                            (i-1,j),            (i+1,j),    
                                            (i-1,j+1),(i,j+1),(i+1,j+1)
                                                ]

        self.disp_window = ax.imshow(self.display_grid)
    
    def step(self):
        display_now = False
        is_done = True
        for i in range(self.width):
            for j in range(self.height):
                trigger = self.check_neighbours_trigger(i, j)
                # print(trigger)
                self.grid[i][j].step(trigger)
                
                is_done = is_done and self.grid[i][j].is_done()

                self.display_grid[i,j] = self.grid[i][j].signal
                if trigger:
                    display_now = True
                # time.sleep(0.01)
        if display_now:
            self.print_grid()
        return is_done
        
    def check_neighbours_trigger(self,i,j):
        # neighbours = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        neighbours = self.four_neighbours(i,j)
        # neighbours = self.eight_neighbours(i,j)
        for neighbour in neighbours:
            _i,_j = neighbour
            if (_i>=0 and _i<self.width) and (_j>=0 and _j<self.height):
                if self.grid[_i][_j].is_triggered():
                    return True
        return False

    def print_grid(self):
        # print("-"*80)
        # print(self.display_grid)
        ax.imshow(self.display_grid)
        # self.disp_window.set_data(self.display_grid)
        # plt.gcf().clear()
        fig.canvas.draw()
        fig.canvas.flush_events()
    
    def run(self):
        tik = 0
        is_done = False
        while not is_done:
            try:
                print("tik:",tik)
                is_done = self.step()
                tik+=1
                
                # self.print_grid()
            except KeyboardInterrupt as e:
                quit()
            except Exception as e:
                traceback.print_exc(e)
                quit()
        print("DONE")


if __name__ == "__main__":
    node_grid = Grid()
    node_grid.run()