import setupVideo
from vars import *

angles = []
velocities = []
fall_guesses = []


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
		if -1 == arr[j] and arr[j - 1] <= angin < arr[j + 1]:
			frames = len(arr) - j
			break

	if arr[j] != arr[j - 1]:

		diffRange = arr[j] - arr[j - 1]
		diffMiddle = angin - arr[j - 1]

		ratio = diffMiddle / diffRange

		if -1 < ratio < 1:
			frames = frames - ratio

	return frames


def hasValInRange(lower, arr, upper):
	for x in arr:
		if lower <= x < upper:
			return True

	return False


def read(readFile):
	arr = []
	with open(path + readFile, 'r') as fd:
		for row in fd:
			lines = row.split(',')
			lines = lines[0:-1]
			lines = [float(x[1:-1]) for x in lines]
			arr = arr + lines

	return arr


# convert angles to velocities
def scanAngles():
	# load angles array to ball_arr
	anglesArrTemp = read(arrFileOut)

	# for each item in ball arr, get the velocity
	i = 1
	while i < len(anglesArrTemp):
		angles.append(anglesArrTemp[i])
		frames = timeForRev(angles, anglesArrTemp[i])

		# write the velocities to arr
		velocities.append(frames)

		setupVideo.write(velocities, velFileOut)

		i += 1


# map velocities to angles difference to fall spot
# aka if you see speed x, it will fall at the current angle + the difference
def mapVelToAngles():
	vels = read(velFileOut)
	angs = read(arrFileOut)[1:]

	map_v2a = {}
	arr_map = [0]

	# init array
	for vel in vels:
		map_v2a[int(vel * 100)] = -1

	# fill angles with the first velocity seen, *100 for more accuracy
	i = 0
	for vel in vels:
		if map_v2a[int(vel * 100)] == -1:
			map_v2a[int(vel * 100)] = (KeyVals[FALL_ANG] - angs[i]) % 360
		i += 1

	# output the map into a tuple array
	i = 0
	for item in map_v2a:
		# print(item, ' = ', map_v2a[item])
		arr_map.append((item, map_v2a[item]))
		i += 0

	setupVideo.write(arr_map, mapFileOut)


# mapVelToAngles()
