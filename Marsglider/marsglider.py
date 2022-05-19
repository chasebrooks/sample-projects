######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

from math import *
from glider import *
import numpy as np
import random
import statistics



OUTPUT_UNIQUE_FILE_ID = False
if OUTPUT_UNIQUE_FILE_ID:
    import hashlib, pathlib
    file_hash = hashlib.md5(pathlib.Path(__file__).read_bytes()).hexdigest()
    print(f'Unique file ID: {file_hash}')

class GliderPositions():

   def __init__(self, height):
      self.num_gliders = 5000
      self.gliders = [(glider(x=round(random.uniform(-250, 250)),
                             y=round(random.uniform(-250, 250)), 
                             z=height, 
                             heading=random.gauss(0, pi/4)),
                       0.0)
                      for i in range(self.num_gliders)]
      self.sigmas = {'importance_sigma': 5, 'x_fuzzing_sigma': 5, 'y_fuzzing_sigma': 5, 'heading_fuzzing_sigma': pi/48}
      self.min_sigmas = {'importance_sigma': 2, 'x_fuzzing_sigma': 2, 'y_fuzzing_sigma': 2, 'heading_fuzzing_sigma': pi/64}
      self.step = 0
      self.oldxy_estimate = (-9999, -9999)
      self.xyestimate = (-9999, -9999) 
      self.converged = False
      self.heading = False
      self.turn_angle = 0.0
      
# The following code is from lecture 8.15: https://classroom.udacity.com/courses/cs373/lessons/48704330/concepts/483118650923
def Gaussian(mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
# end copied code

def estimate_next_pos(height, radar, mapFunc, OTHER=None):
   """Estimate the next (x,y) position of the glider."""
   # initialize glider positions
   if OTHER == None:
      OTHER = GliderPositions(height)

   # create importance weights

   OTHER.gliders = [(glider[0], Gaussian((glider[0].z - mapFunc(glider[0].x, glider[0].y)), OTHER.sigmas['importance_sigma'], radar)) for glider in OTHER.gliders]
   OTHER.gliders = sorted(OTHER.gliders, key=lambda x: x[1], reverse=True)

   # decay importance sigma every 10 iterations
   OTHER.sigmas['importance_sigma'] = max(OTHER.sigmas['importance_sigma']*.98, OTHER.min_sigmas['importance_sigma'])

   # Resample
   # The following code is from lecture 8.21: 
   p2 = []
   N = len(OTHER.gliders)
   index = int(random.random() * N)
   beta = 0.0
   mw = max([i[1] for i in OTHER.gliders])
   for i in range(max(int(N*.99), 3000)):
      beta += random.random() * 2.0 * mw
      while beta > OTHER.gliders[index][1]:
         beta -= OTHER.gliders[index][1]
         index = (index + 1) % N
      p2.append(OTHER.gliders[index])
   # End copied code
   particles = [i for i in p2]
   

   # Fuzz
   fuzzed_particles = []
   x_sigma = OTHER.sigmas['x_fuzzing_sigma']
   y_sigma = OTHER.sigmas['y_fuzzing_sigma']
   heading_sigma = OTHER.sigmas['heading_fuzzing_sigma']

   for particle in particles:
      particle[0].x += random.gauss(0, x_sigma)
      particle[0].y += random.gauss(0, y_sigma)
      particle[0].heading += random.gauss(0, heading_sigma)
      fuzzed_particles.append(particle)

   OTHER.sigmas['x_fuzzing_sigma'] = max(OTHER.sigmas['x_fuzzing_sigma']*.98, OTHER.min_sigmas['x_fuzzing_sigma'])
   OTHER.sigmas['y_fuzzing_sigma'] = max(OTHER.sigmas['y_fuzzing_sigma']*.98, OTHER.min_sigmas['y_fuzzing_sigma'])
   OTHER.sigmas['heading_fuzzing_sigma'] = max(OTHER.sigmas['heading_fuzzing_sigma']*.98, OTHER.min_sigmas['heading_fuzzing_sigma'])

   # glide particles
   out_particles = [(particle[0].glide(rudder=OTHER.turn_angle), particle[1]) for particle in fuzzed_particles]
   
   OTHER.gliders = out_particles

   # weighted average
   # total_weights = sum([particle[1] for particle in OTHER.gliders])
   # pred_x = sum([particle[0].x * particle[1] for particle in OTHER.gliders]) / total_weights
   # pred_y = sum([particle[0].y * particle[1] for particle in OTHER.gliders]) / total_weights

   # median
   pred_x = statistics.median([particle[0].x for particle in OTHER.gliders])
   pred_y = statistics.median([particle[0].y for particle in OTHER.gliders])

   # simple average
   # pred_x = sum([particle.x for particle in OTHER.gliders])/len(OTHER.gliders)
   # pred_y = sum([particle.y for particle in OTHER.gliders])/len(OTHER.gliders)
 
   xy_estimate = (pred_x, pred_y) 
   
   if OTHER.step > 0:
      euclidean_distance = sqrt(((OTHER.xyestimate[0] - xy_estimate[0]) ** 2) + (OTHER.xyestimate[1] - xy_estimate[1]) ** 2)
      if euclidean_distance < 10 and OTHER.step >= 35:
         OTHER.converged = True
         OTHER.heading = sum([particle[0].heading for particle in OTHER.gliders])/len(OTHER.gliders)
   
   OTHER.xyestimate = xy_estimate

   optionalPointsToPlot = [(particle[0].x, particle[0].y, particle[0].heading) for particle in OTHER.gliders]  #(x,y,heading)

   OTHER.step += 1
   
   return xy_estimate, OTHER, optionalPointsToPlot


def next_angle(height, radar, mapFunc, OTHER=None):

   xy_estimate, OTHER, optionalPointsToPlot = estimate_next_pos(height, radar, mapFunc, OTHER)
   if OTHER.converged == True:

      target_heading = (np.arctan2(-xy_estimate[1], -xy_estimate[0])) % (2 * pi)

      current_heading = sum([particle[0].heading for particle in OTHER.gliders])/len(OTHER.gliders)
      # Following code adapted from stackoverflow: https://stackoverflow.com/questions/37358016/numpy-converting-range-of-angles-from-pi-pi-to-0-2pi
      current_heading = ((2*pi + current_heading)*(current_heading < 0)) + (current_heading)*(current_heading > 0)
      # end copied code

      steering_angle = target_heading - current_heading
      OTHER.turn_angle = steering_angle

   else: 
      steering_angle = pi/12
      OTHER.turn_angle = steering_angle
   
   OTHER.oldxy_estimate = xy_estimate

   return steering_angle, OTHER, optionalPointsToPlot

def who_am_i():
    # Please specify your GT login ID in the whoami variable (ex: jsmith221).
    whoami = 'dbrooks43'
    return whoami
