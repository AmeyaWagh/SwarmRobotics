#!/bin/python3
import moviepy.editor as mpy


similarity_thresholds = [float(i)/10.0 for i in range(1, 10, 1)]
gif_name = 'schelling_model'
fps = 2
file_list = ['out/schelling_2_{}_final.png'.format(int(_thresh*100)) for  _thresh in similarity_thresholds]
print (file_list)
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif('{}.gif'.format(gif_name), fps=fps)