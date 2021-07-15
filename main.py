import numpy as np
import cv2
import math

vid = []
orgVid = []
ball_arr = [0]
times = [0]
path = "C:\\Users\\Zander\\Desktop\\roulette\\resources\\"
fileIn = "spin5"
fileOut = "outputArr.txt"
extension = ".mp4"
cap = cv2.VideoCapture(path + fileIn + extension)

UI = False

e = 2.71828

center = (550, 360)
fRate = 30
timer = 0
on = False


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
	trim_tl = (0, 20)  # x y
	trim_br = (width, height - 10)  # x y
	frame = frame[trim_tl[1]:trim_br[1], trim_tl[0]:trim_br[0]]  # y y x x

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

	subbed = tmp
	height, width, z = tmp.shape
	inner = int(height * 0.435)

	# fill inner circle
	subbed = cv2.circle(subbed, center, inner, (0, 0, 0), -1)
	subbed = cv2.subtract(subbed, last)  # get change between frames (moving)

	# convert to grey, blue to get bigger items, get brightest point
	subbed = cv2.cvtColor(subbed, cv2.COLOR_RGB2GRAY)
	subbed = cv2.GaussianBlur(subbed, (21, 21), 0)
	limit = subbed.max()

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

	subbed = cv2.inRange(subbed, np.array([int(lower)]), np.array([upper]))
	cv2.findNonZero(subbed)  # list of all non 0 points
	contours, hierarchy = cv2.findContours(subbed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # biggest non zero area

	c = []
	if len(contours) != 0:
		# draw in blue the contours that were founded
		cv2.drawContours(subbed, contours, -1, 255, 3)

		# find the biggest contour (c) by the area
		c = max(contours, key=cv2.contourArea)

	t_q = (0, 0)
	t_a = 360

	# get farthest clockwise point in contour = t _ a
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

# no inspection PyTupleAssignmentBalance
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

	ball_arr = ball_arr[3:-1]

	times = [x for x in range(len(ball_arr))]
	lower = times[0]
	times = [x - lower for x in times]
	time_total = times[len(times) - 1]
	best_fit = np.poly1d(np.polyfit(times, ball_arr, 3))

	import matplotlib.pyplot as plt
	xp = np.linspace(0, time_total, time_total)
	_ = plt.plot(times, ball_arr, '.', xp, best_fit(xp))

	plt.show()


main()
