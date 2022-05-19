import random
from glider import *
import numpy as np

# (80.83218540276988, 802.2215408648027) (83.52602106686174, 804.4516689562034)
# current heading:  0.6915014532557511
# steering angle:  2.4500912003340423 

def Gaussian(mu, sigma, x):
    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
# end copied code

# 5092.054082173813 [([-125.16, -73.72, 4965.48], 0.07978036315238263),




print(Gaussian(4755, 4.9, 4668))