
from lib.SchellingModel import Schelling
import os
import traceback
import moviepy.editor as mpy


class experimentFactory(object):
    def __init__(self, exp_type, exp_name):
        self.exp_type   = exp_type
        self.exp_name   = exp_name
        self.model      = None
        self.result_path = "./out/{}".format(self.exp_name)
        self.__create_experiment_env()

    def create_experiment(self, config={}):
        if self.exp_type == "SchellingModel":
            try:
                self.model = Schelling(**config)
            except Exception as e:
                traceback.print_exc(e)
        else:
            print("experiment not found!!")

    def perform_experiment(self):
        print(self.model)
        self.results = self.model.perform(   result_path = self.result_path,
                                            n_result_steps = 3)

    def __create_experiment_env(self):
        print("creating environment")
        if not os.path.isdir(self.result_path):
            os.makedirs(self.result_path)

    def create_gif(self):
        clip = mpy.ImageSequenceClip(self.results, fps=1)
        clip.write_gif(os.path.join(    self.result_path,
                                        '{}.gif'.format(self.exp_name)), 
                                        fps=1)
