from src.vars import *

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
		if -1 == arr[j] and arr[j-1] <= angin < arr[j+1]:
			frames = len(arr) - j
			break

	if arr[j] != arr[j-1]:

		diffRange = arr[j]-arr[j-1]
		diffMiddle = angin - arr[j-1]

		ratio = diffMiddle/diffRange

		if -1 < ratio < 1:
			frames = frames - ratio

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


# with open(path + arrFileOut, 'r') as fd:
# 	for row in fd:
# 		lines = row.split(',')
# 		lines = lines[0:-1]
# 		lines = [float(x[1:-1]) for x in lines]
# 		ball_arr = ball_arr + lines
#
#
# i = 1
# while i < len(ball_arr):
# 	scan(ball_arr[i])
#
# 	i += 1
#
# time_total = times[len(times)-1]
