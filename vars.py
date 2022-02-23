import numpy as np
from scipy import optimize
import cv2
import math
import matplotlib.pyplot as plt

# Finals
path = "C:\\Users\\Zander\\IdeaProjects\\roulette2\\Resources\\"
# path = "C:\\Users\\Zander\\Desktop\\roulette\\resources\\"
fileIn = "spin3"
fileOut = "outputArr.txt"
extension = ".mp4"

e = 2.71828
center = (550, 360)
fRate = 30

# variables
vid = []
orgVid = []
ball_arr = [0]
times = [0]
timer = 0
on = False

# best fit as calculated
best_fit_final = np.poly1d([1.915e-09, - 1.996e-06, 0.0006397, 0.04803, 10.59])
drop_speed_final = 65.471835446875
target_velocities = [12.90, 15.0, 16.0, 16.73, 18.0, 21, 26.0, 29, 35, 37.06, 37.87, 51.73, 65.0]

#start fall stop fallang
START = 0
FALL = 1
STOP = 2
FALL_ANG = 3
KeyVals = [20,537,627,75.96] #spin3