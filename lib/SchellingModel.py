"""
code inspired from "https://www.binpress.com/simulating-segregation-with-python/"

"""

import matplotlib.pyplot as plt
import itertools
import random
import copy
import os

class Schelling:
    def __init__(   self,  
                    width=50, height=50, 
                    population_frac         = 0.5, 
                    similarity_threshold    = 3,
                    n_neighbors             = 8, 
                    n_iterations            = 500, 
                    races                   = 2
                ):

        self.width          = width 
        self.height         = height 
        self.races          = races
        self.population_frac    = population_frac
        self.empty_ratio    = 1.0 - self.population_frac
        self.n_neighbors    = n_neighbors
        self.similarity_threshold = float(similarity_threshold)/float(n_neighbors)
        self.n_iterations   = n_iterations
        self.empty_houses   = []
        self.agents         = {}
        self.result_sequence = []
        self.__populate()
 
    def __populate(self):
        self.all_houses = list(itertools.product(range(self.width),range(self.height)))
        random.shuffle(self.all_houses)
     
        self.n_empty        = int( self.empty_ratio * len(self.all_houses) )
        self.empty_houses   = self.all_houses[:self.n_empty]
     
        self.remaining_houses = self.all_houses[self.n_empty:]
        houses_by_race = [self.remaining_houses[i::self.races] for i in range(self.races)]
        for i in range(self.races):
            #create agents for each race
            self.agents = dict(
                                self.agents.items() +
                                dict(zip(houses_by_race[i], [i+1]*len(houses_by_race[i]))).items()
                                )
 
    def is_unsatisfied(self, x, y): 
        race = self.agents[(x,y)]
        count_similar = 0
        count_different = 0
     
        if x > 0 and y > 0 and (x-1, y-1) not in self.empty_houses:
            if self.agents[(x-1, y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if y > 0 and (x,y-1) not in self.empty_houses:
            if self.agents[(x,y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width-1) and y > 0 and (x+1,y-1) not in self.empty_houses:
            if self.agents[(x+1,y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and (x-1,y) not in self.empty_houses:
            if self.agents[(x-1,y)] == race:
                count_similar += 1
            else:
                count_different += 1        
        if x < (self.width-1) and (x+1,y) not in self.empty_houses:
            if self.agents[(x+1,y)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height-1) and (x-1,y+1) not in self.empty_houses:
            if self.agents[(x-1,y+1)] == race:
                count_similar += 1
            else:
                count_different += 1        
        if x > 0 and y < (self.height-1) and (x,y+1) not in self.empty_houses:
            if self.agents[(x,y+1)] == race:
                count_similar += 1
            else:
                count_different += 1        
        if x < (self.width-1) and y < (self.height-1) and (x+1,y+1) not in self.empty_houses:
            if self.agents[(x+1,y+1)] == race:
                count_similar += 1
            else:
                count_different += 1
     
        if (count_similar+count_different) == 0:
            return False
        else:
            return float(count_similar)/(count_similar+count_different) < self.similarity_threshold
 
    def update(self, result_path, n_result_steps=3):
        self.plot("{}".format(self.__str__()),os.path.join(result_path,"initial.png"))
        self.result_sequence.append(os.path.join(result_path,"initial.png"))

        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            for agent in self.old_agents:
                if self.is_unsatisfied(agent[0], agent[1]):
                    agent_race = self.agents[agent]
                    empty_house = random.choice(self.empty_houses)
                    self.agents[empty_house] = agent_race
                    del self.agents[agent]
                    self.empty_houses.remove(empty_house)
                    self.empty_houses.append(agent)
                    n_changes += 1
            print("[n_changes]{}".format(n_changes))
            if n_changes == 0:
                break

            if i%n_result_steps == 0:
                __path = os.path.join(result_path,"final_{}.png".format(i))
                self.plot("{} iteration {}".format(self.__str__(), i),
                            __path)
                self.result_sequence.append(__path)

        self.plot("{}".format(self.__str__()),os.path.join(result_path,"final.png"))
        self.result_sequence.append(os.path.join(result_path,"final.png"))

 
    def move_to_empty(self, x, y):
        race = self.agents[(x,y)]
        empty_house = random.choice(self.empty_houses)
        self.updated_agents[empty_house] = race
        del self.updated_agents[(x, y)]
        self.empty_houses.remove(empty_house)
        self.empty_houses.append((x, y))
     
    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        #If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
        agent_colors = {    1:'b', 
                            2:'r', 
                            3:'g', 
                            4:'c', 
                            5:'m', 
                            6:'y', 
                            7:'k'
                        }

        for agent in self.agents:
            ax.scatter(agent[0]+0.5, agent[1]+0.5, color=agent_colors[self.agents[agent]])
     
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

    def perform(self, result_path="./", n_result_steps=3):
        self.update(result_path, n_result_steps)
        return self.result_sequence

    def __str__(self):
        __doc = "Schelling Model with grid size:{} \n population fraction:{} \n and satisfaction threshold {} \n".format(tuple((self.width, self.height)),
            self.population_frac,
            self.similarity_threshold*self.n_neighbors)
        return __doc