import numpy as np

from vars import *
import matplotlib.pyplot as plt

angles = []
times = []

def getChange(arr):
	out =[]
	i = 1
	while i < len(ball_arr):
		dif = ball_arr[i]-ball_arr[i-1]
		if dif > 200:
			dif = 360 - dif
		if dif < - 200:
			dif = 360 + dif
		out.append(dif)
		i += 1

	return out


def getDirection(arr):
	pos = 0
	neg = 0
	for i in arr:
		if i > 0:
			pos += 1
		else:
			neg += 1

	out = arr
	if pos < neg:
		out = [-x for x in arr]  # invert entire array if neg

	print("pos", pos, " neg",neg)

	return out



def clearNeg(arr):
	out = []
	for i in arr:
		if i < 0:
			i = -1
		out.append(i)

	return out

def clearHighTEMP(arr):
	out = []
	for i in arr:
		if i > 100:
			i = -1
		out.append(i)

	return out

def trimSD(arr):
	out = []

	SDlim = 1

	i = 0
	for _ in arr:

		std = np.std(arr[i:i+10])
		mean = np.mean(arr[i:i+10]) # mean throws error

		for y in arr[i:i+10]:
			if mean - (std*SDlim) < y < mean + (std*SDlim):
				out.append(y)
			else:
				out.append(-1)

		i += 10

	return out

def timeForRev(arr,angin):
	frames = -1

	j = len(arr)
	while j > 1:

		j = j - 1
		if arr[j - 1] < angin < arr[j] and arr[j-1] != 0:
			frames = len(arr) - j
			break

	if 0 < frames < 30:
		print(frames, " arr ", [int(x) for x in arr[-30:]] , " ang ", int(angin))

	return frames

def scan(ang):
	angles.append(ang)
	times.append(timeForRev(angles, ang))


with open(path + fileOut, 'r') as fd:
	for row in fd:
		lines = row.split(',')
		lines = lines[0:-1]
		lines = [float(x[1:-1]) for x in lines]
		ball_arr = ball_arr + lines

# a = getChange(ball_arr)
# b = getDirection(a)
# c = clearNeg(b)
# d = clearHighTEMP(c)
# e = timePreRev(d)


# print(display)


i = 1
while i < len(ball_arr):

	scan(ball_arr[i])

	i += 1

displayBefore = [x/5 for x in angles]
displayAfter = trimSD(times)
plt.plot([x for x in range(len(displayBefore))], displayBefore, '.')
plt.plot([x for x in range(len(displayAfter))], displayAfter, '.') # , plt.ylim([0, 50])
# plt.plot(times, [x/10 for x in angles[0:-1]], '-')

plt.show()
#

# look at kalman filter
# shutter effect makes a non-sin wave, really hard to avoid
# probably use time since last in that position to negate shutter effect
