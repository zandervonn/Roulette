import numpy as np

from vars import *
import matplotlib.pyplot as plt

angles = []
velocities = []
timesSmooth = []
fall_guesses = []

# best fit as calculated
best_fit_final = np.poly1d([1.915e-09, - 1.996e-06, 0.0006397, 0.04803, 10.59])
drop_speed_final = 65.471835446875
target_velocities = [12.90, 15.0, 16.0, 16.73, 18.0, 21, 26.0, 29, 35, 37.06, 37.87, 51.73, 65.0]


def timeForRev(arr, angin):
	frames = -1

	j = len(arr) - 1
	# for all in array
	while j > 1:
		# iterate
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

	#  adjust frames int, into the ratio between values found

	#  if arr[j] != arr[j-1] and frames != -1 and arr[j] != -1:
	if arr[j] != arr[j-1]:

		diffRange = arr[j]-arr[j-1]
		diffMiddle = angin - arr[j-1]

		ratio = diffMiddle/diffRange

		if -1 < ratio < 1:
			frames = frames - ratio

			# print("arrj" ,arr[j], "arrj-1", arr[j-1], "diffRange" ,diffRange, "diffMiddle" ,diffMiddle, "ratio" ,ratio)
			# print("ratio: " ,ratio)

	# target = 0.5
	# if arr[j]> target > arr[j - 1]:
	# 	print("@", angin, " vel =", frames)

	return frames


def getPairArrays(x):
	out_x = []
	out_y = []

	i = 0
	for val in x:
		if val > 3:  # three to pick up any small jiggles
			out_y.append(val)
			out_x.append(i)

		i += 1

	return out_x, out_y


def hasValInRange(lower, arr, upper):

	for x in arr:
		if lower <= x < upper:
			return True

	return False


def getAverageAngle(arr):
	x = 0
	y = 0
	for val in arr:
		x += math.sin(math.radians(val))
		y += math.cos(math.radians(val))

	return math.degrees(math.atan2(x, y)) % 365

def scan(ang):
	angles.append(ang)
	frames = timeForRev(angles, ang)

	if len(velocities) > 1:
		if hasValInRange(velocities[-1], target_velocities, frames):
			fall_guesses.append(ang)
			print(f"It will fall HERE!!! ({ang}) = {getAverageAngle(fall_guesses)}")

	velocities.append(frames)


with open(path + fileOut, 'r') as fd:
	for row in fd:
		lines = row.split(',')
		lines = lines[0:-1]
		lines = [float(x[1:-1]) for x in lines]
		ball_arr = ball_arr + lines


def smooth(y, box_pts):
	box = np.ones(box_pts)/box_pts
	y_smooth = np.convolve(y, box, mode='same')
	return y_smooth

# not working
def trimEnds(arr, ttt):

	best_fit = np.poly1d(np.polyfit(ttt, arr, 4))
	std = np.std(arr)
	buffer = 0.5

	while True:
		i = 0
		print("pop bottom", len(arr),"i = ", i, " guess = ", best_fit(ttt[i]), " real = ", arr[i],  "avg = ", std)
		if best_fit(ttt[i]) - (std*buffer) >  arr[i] or best_fit(ttt[i]) + (std*buffer) <  arr[i]:
			arr.pop(i)
			ttt.pop(i)

		else:
			break

	while True:
		i = len(arr) - 1
		print("pop top", len(arr),"i = ", i, " guess = ", best_fit(ttt[i]), " real = ", arr[i],  "avg = ", std)
		if best_fit(ttt[i]) - (std*buffer) >  arr[i] or best_fit(ttt[i]) + (std*buffer) <  arr[i]:
			ttt.pop(i)

		else:
			break

i = 1
while i < len(ball_arr):
	scan(ball_arr[i])

	i += 1

#  get x and y of points
times, displayBefore = getPairArrays(velocities)

print(displayBefore)

# display points
# plt.plot([x for x in range(len(displayBefore))], trimEnds(displayBefore, times), '.')

# get best fit
best_fit = np.poly1d(np.polyfit(times, displayBefore, 4))
# best_fit = best_fit_final
print("Best fit:\t", best_fit , "\t/best fit")
time_total = times[len(times)-1]

print("final speed= ", best_fit_final(time_total))

# display best fit
xp = np.linspace(0, time_total, time_total)
_ = plt.plot(times, displayBefore,  '.', xp, best_fit(xp))

plt.show()

# find drop point, and all the velocities that it crosses this point before
# then you know key velocities to look out for
