import numpy as np
from scipy import optimize
import cv2
import math
import matplotlib.pyplot as plt

# Finals
path = "./Resources\\"
# path = "C:\\Users\\Zander\\Desktop\\roulette\\Resources\\"
fileIn = "spin5"
arrFileOut = "outAnglesArr.txt"
velFileOut = "outVelocitiesArr.txt"
mapFileOut = "outMappingArr.txt"
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
CLOCKWISE = 4

if fileIn == "spin3": KeyVals = [20, 537, 627, 75.96, 0]
if fileIn == "spin4": KeyVals = [20, 537, 627, 75.96, True] #guess
if fileIn == "spin5": KeyVals = [69, 599, 687, 0.00000, 0]
if fileIn == "spin7": KeyVals = [35, 617, 679, 100.00000, 0]