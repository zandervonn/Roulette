import numpy as np

from vars import *
import matplotlib.pyplot as plt

angles = []
times = []
timesSmooth = []

def timeForRev(arr, angin):
	frames = -1

	j = len(arr) - 1
	# for all in array
	while j > 1:
		# itterate
		j = j - 1

		# deal with poles on gap bigger than 180
		if arr[j - 1] - arr[j] > 180 and (arr[j - 1] <= angin < 360 or 0 <= angin < arr[j]):
			frames = len(arr) - j
			break

		# find the last occurrence where the value is between
		if -1 != arr[j - 1] <= angin < arr[j] != -1:
			frames = len(arr) - j
			break

		# on -1 aka error
		if -1 == arr[j] and arr[j-1] <= angin < arr[j+1]:
			frames = len(arr) - j
			break

	# print(frames, " arr ", [int(x) for x in arr[-140:]], " ang ", int(angin))

	return frames


def scan(ang):
	angles.append(ang)
	frames = timeForRev(angles, ang)

	times.append(frames)
	# timesSmooth.append(avgSlope(times))


with open(path + fileOut, 'r') as fd:
	for row in fd:
		lines = row.split(',')
		lines = lines[0:-1]
		lines = [float(x[1:-1]) for x in lines]
		ball_arr = ball_arr + lines

i = 1
while i < len(ball_arr):
	scan(ball_arr[i])

	i += 1

displayBefore = times
displayAfter = timesSmooth

plt.plot([x for x in range(len(displayBefore))], displayBefore, '.')
plt.plot([x for x in range(len(displayAfter))], displayAfter, '.')

plt.show()
#


# find drop point, and all the velocities that it crosses this point before
# then you know key velocities to look out for
