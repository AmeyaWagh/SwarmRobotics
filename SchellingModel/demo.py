
#!/bin/python

from lib.SchellingModel import Schelling
import os

if __name__ == '__main__':

    similarity_thresholds = [float(i)/10.0 for i in range(1, 10, 1)]

    schelling_1 = Schelling(50, 50, 0.3, similarity_thresholds[0], 500, 2)
    schelling_1.populate()
    if not os.path.isdir("./out"):
        os.makedirs("./out")

    schelling_1.plot('Schelling Model with 2 colors: Initial State', 'out/schelling_2_initial.png')
    for _thresh in similarity_thresholds:
        schelling_1 = Schelling(50, 50, 0.3, _thresh, 500, 2)
        schelling_1.populate()
        schelling_1.update() 
        schelling_1.plot('Schelling Model with 2 colors: Final State with Similarity Threshold {} %'.format(int(_thresh*100)), 'out/schelling_2_{}_final.png'.format(int(_thresh*100)))
