import numpy as np
import cv2
import math
from scipy.integrate import quad

vid = []
orgVid = []
ball_arr = [0]
times = [0]
path = "C:\\Users\\Zander\\Desktop\\roulette\\resources\\"
fileIn = "spin5"
fileOut = "outputArr.txt"
extention = ".mp4"
cap = cv2.VideoCapture(path + fileIn + extention)

UI = False

e = 2.71828

center = (550, 360)
fRate = 30
timer = 0
on = False


def write(arr):
	text_file = open(path + fileOut, "w")
	i = 1
	for element in arr:

		text_file.write('[' + str(int(element)) + '],')
		if i % 4 == 0:
			text_file.write('\n')
		i = i + 1
	text_file.close()


def get_frames():
	while cap.isOpened():
		loop, frame = cap.read()

		if loop:

			frame = overlay(frame)

			vid.append(frame)
			orgVid.append(frame)

		else:
			break


def overlay(frame):
	height, width, channels = frame.shape

	# trim frame
	trim_tl = (0, 20)  # xy
	trim_br = (width, height - 10)  # xy
	frame = frame[trim_tl[1]:trim_br[1], trim_tl[0]:trim_br[0]]  # yyxx

	frame = cv2.resize(frame, (width - 90, height))

	# outside circle
	mask = np.zeros_like(frame)
	mask = cv2.circle(mask, center, int(height / 2), (255, 255, 255), -1)
	frame = cv2.bitwise_and(frame, mask)

	# green circle
	frame = cv2.circle(frame, center, 2, (0, 0, 255), -1)
	frame = cv2.circle(frame, center, int(height / 2), (0, 0, 255), 1)

	# ball circle
	inner = int(height * 0.435)
	frame = cv2.circle(frame, center, inner, (255, 0, 0), 1)

	return frame


def getBall(tmp, last, frame):
	global timer, ball_arr, times, on

	subed = tmp
	height, width, z = tmp.shape
	inner = int(height * 0.435)

	# fill inner circle
	subed = cv2.circle(subed, center, inner, (0, 0, 0), -1)
	subed = cv2.subtract(subed, last)  # get change between frames (moving)

	# conv to grey, blue to get bigger items, get brightest point
	subed = cv2.cvtColor(subed, cv2.COLOR_RGB2GRAY)
	subed = cv2.GaussianBlur(subed, (21, 21), 0)
	limit = subed.max()

	# rangeT from brightest point that may be ball
	range_t = 20

	if limit < 7:
		limit = 255
	lower = limit
	upper = limit + 1
	if limit > range_t:
		lower = lower - range_t
	else:
		lower = int(limit / 2)

	subed = cv2.inRange(subed, np.array([int(lower)]), np.array([upper]))
	cv2.findNonZero(subed)  # list of all non 0 points
	contours, hierarchy = cv2.findContours(subed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # biggest non zero area

	c = []
	if len(contours) != 0:
		# draw in blue the contours that were founded
		cv2.drawContours(subed, contours, -1, 255, 3)

		# find the biggest countour (c) by the area
		c = max(contours, key=cv2.contourArea)

	t_q = (0, 0)
	t_a = 360

	# get farthest clockwise point in contour
	if c is not None and len(c) > 1:
		for x in c:
			for p in x:
				a = getAngle(p)
				if a < t_a:
					t_q = p
					t_a = a

		# get when the ball first crosses into angles
		lower = 200
		upper = 359
		if lower < t_a < upper:
			if not on:
				ttt = (frame * fRate) - times[-1:][0]
				mod = (t_a / 360) - (lower / 360)
				out = ttt + (ttt * mod)  # time + 1.x, x% way past 180
				print("180+.. time = ", int(ttt), " mod = %", int(100 * mod), " out = ", int(out))
				ball_arr.append(out)

			on = True

		else:
			on = False

	return t_q


def getAngle(point):
	c_x = center[0]
	c_y = center[1]
	x = point[0]
	y = point[1]

	x = x - c_x
	y = y - c_y

	ang = 180 + (180 * (math.atan2(x, y) / math.pi))

	if ang != 45:
		return ang
	else:
		return 0


def key(k):
	if cv2.waitKey(25) & 0xFF == ord(k):
		return True


def solve_y(poly, y):
	poly_arr = poly.c
	if len(poly_arr) != 2:
		return 0

	x = y - poly_arr[1]
	x = x / poly_arr[0]
	return x


# noinspection PyTupleAssignmentBalance
def main():
	global times, ball_arr
	get_frames()

	i = 0
	while i < len(vid) - 1:
		if i > 0:  # skip early frames
			vid[i].copy()

			b = getBall(vid[i], vid[i - 1], i + 1)

			cv2.circle(orgVid[i], (int(b[0]), int(b[1])), 5, (100, 255, 50), -1)

			if UI:
				cv2.imshow("Display", orgVid[i])
				cv2.waitKey(int(1000 / fRate))  # sync frame rate

		i = i + 1

	times = []
	times = [x for x in range(len(ball_arr))]

	ball_arr.pop(0)
	times.pop(0)

	ball_arr_log = [math.log(x, e) for x in ball_arr if x > 0]
	best_fit = np.poly1d(np.polyfit(times, ball_arr_log, 1))

	write(ball_arr)

	total = 0
	i = 0
	while i < len(ball_arr_log) - 1:
		total += abs(ball_arr_log[i] - best_fit(times[i]))
		i = i + 1
	avg = total / len(ball_arr_log)

	range_t = 0.5

	while True:
		i = 0
		print("pop bottom", len(ball_arr_log), "i = ", i, " guess = ", best_fit(times[i]), " real = ", ball_arr_log[i], "avg = ", avg * range_t)
		if best_fit(times[i]) - (avg * range_t) > ball_arr_log[i] or best_fit(times[i]) + (avg * range_t) < ball_arr_log[i]:
			ball_arr_log.pop(i)
			times.pop(i)

		else:
			break

	while True:
		i = len(ball_arr_log) - 1
		print("pop top", len(ball_arr_log), "i = ", i, " guess = ", best_fit(times[i]), " real = ", ball_arr_log[i], "avg = ", avg * range_t)
		if best_fit(times[i]) - (avg * range_t) > ball_arr_log[i] or best_fit(times[i]) + (avg * range_t) < ball_arr_log[i]:
			ball_arr_log.pop(i)
			times.pop(i)

		else:
			break

	# build_graph

	# ball_arr_log = [(1000/(2.71828 ** x)) for x in ball_arr_log]

	lower = times[0]
	times = [x - lower for x in times]
	time_total = times[len(times) - 1]
	best_fit = np.poly1d(np.polyfit(times, ball_arr_log, 1))

	# print("Best fit:\t", best_fit , "\t/best fit")
	import matplotlib.pyplot as plt
	xp = np.linspace(0, time_total, time_total)
	_ = plt.plot(times, ball_arr_log, '.', xp, best_fit(xp))

	# print("rps start = ", (best_fit(0)))
	print("rps start = ", 1 / (e ** best_fit(0)))
	# print("rps at fall = ", (best_fit(len(ball_arr_log))))
	print("rps at fall = ", 1 / (e ** best_fit(len(ball_arr_log))))

	def f(x):
		return 1 / (e ** best_fit(x))

	res, err = quad(f, 0, time_total)
	print("spins?? =", len(ball_arr_log))
	print("REVOLUTIONS: = ", res)

	print("angle of fall, relitive to spin start =", (res - math.floor(res)) * 360)

	plt.show()


main()

# need to find the equilizer speed. aka the speed it is going when it crosses its final number.
# ^^ could be done with equilizer point on rim, to calculate langing point later
# ^^ this is probably better as it takes bounce varience out of it. just add a typical bounce distance
#
# rmp = rmp ball + rpm inner
# start = 0 = green - x
# finish = +- y (green - x, realitive at fall) ?? or do you just take the num where it ends
#
# ball drop @ avg - 30ms, or just lowest found speed
# see how well different runs line up with same drop point
#
# angle past check mod not working??

# 3000
# 8000
# 21000
# 55000
# 150000
# 400000
# 1000000
# 2800000
# 7000000
# 18500000
