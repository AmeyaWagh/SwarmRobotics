#!/bin/python

from lib.experimentFactory import experimentFactory
import os
import inspect


CONFIG = {  
            "width":50, 
            "height":50, 
            "population_frac":0.5, 
            "similarity_threshold":3,
            "n_neighbors":8, 
            "n_iterations":500
        }

if __name__ == '__main__':


    exp1 = experimentFactory("SchellingModel","SchellingModel_1")
    exp1.create_experiment(CONFIG)
    exp1.perform_experiment()
    exp1.create_gif()
    del exp1

    CONFIG["population_frac"] = 0.9
    CONFIG["similarity_threshold"] = 3
    exp2 = experimentFactory("SchellingModel","SchellingModel_2")
    exp2.create_experiment(CONFIG)
    exp2.perform_experiment()
    exp2.create_gif()
    del exp2

    CONFIG["population_frac"] = 0.5
    CONFIG["similarity_threshold"] = 4
    exp3 = experimentFactory("SchellingModel","SchellingModel_3")
    exp3.create_experiment(CONFIG)
    exp3.perform_experiment()
    exp3.create_gif()
    del exp3

    CONFIG["population_frac"] = 0.9
    CONFIG["similarity_threshold"] = 4
    exp4 = experimentFactory("SchellingModel","SchellingModel_4")
    exp4.create_experiment(CONFIG)
    exp4.perform_experiment()
    exp4.create_gif()
    del exp4

