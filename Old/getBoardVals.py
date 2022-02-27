from vars import *
import matplotlib.pyplot as plt

angles = []
velocities = []


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

	#  adjust frames int, into the ratio between values found
	if arr[j] != arr[j-1]:

		diffRange = arr[j]-arr[j-1]
		diffMiddle = angin - arr[j-1]

		ratio = diffMiddle/diffRange

		if -1 < ratio < 1:
			frames = frames - ratio

	target = 0.5
	if arr[j]> target > arr[j - 1]:
		print("@", angin, " vel =", frames)

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


def scan(ang):
	angles.append(ang)
	frames = timeForRev(angles, ang)
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
# #  get x and y of points
# times, displayBefore = getPairArrays(velocities)
#
# print(displayBefore)
#
# # display points
# # plt.plot([x for x in range(len(displayBefore))], trimEnds(displayBefore, times), '.')
#
# # get best fit
# best_fit = np.poly1d(np.polyfit(times, displayBefore, 4))
#
# # best_fit = best_fit_final
# print("Best fit:\t", best_fit , "\t/best fit")
# time_total = times[len(times)-1]
#
# # display points and best fit line
# xp = np.linspace(0, time_total, time_total)
# _ = plt.plot(times, displayBefore,  '.', xp, best_fit(xp))
#
# print("final speed= ", best_fit(time_total))
#
# plt.show()
