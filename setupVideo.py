from vars import *

cap = cv2.VideoCapture(path + fileIn + extension)

angles = []


def get_frames():
	while cap.isOpened():
		loop, frame = cap.read()

		if loop:

			frame = overlay(frame)

			vid.append(frame)
			orgVid.append(frame)

		else:
			break


def write(arr, pathOut):
	text_file = open(path + pathOut, "w")
	i = 1
	for element in arr:

		text_file.write('[' + str(element) + '],')
		if i % 4 == 0:
			text_file.write('\n')
		i = i + 1
	text_file.close()


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
		return -1


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

		angles.append(t_a)
		# get when the ball first crosses into angles
		lower = 200
		upper = 359
		if lower < t_a < upper:
			if not on:
				ttt = (frame * fRate) - times[-1:][0]
				mod = (t_a / 360) - (lower / 360)
				out = ttt + (ttt * mod)  # time + 1.x, x% way past 180
				ball_arr.append(out)
				times.append(frame * fRate)

			on = True

		else:
			on = False

	return t_q


# scan the video for key frames
# a = forward
# d = forward
# r = stop
# w = capture frame
def getKeyFrames():
	get_frames()

	i_max = len(orgVid)
	i = 0
	while True:

		if i < 0: i = 0
		if i > i_max: i = i_max
		cv2.imshow("Display", orgVid[i])

		key = cv2.waitKey(33)
		if key == ord('d'): i += 1
		if key == ord('a'): i -= 1
		if key == ord('w'): print(i)
		if key == ord('r'): break


# get the list of angles of the ball for the scanned video
def getAngles():
	get_frames()

	# load key frames
	f_start = KeyVals[START]
	f_fall = KeyVals[FALL]

	# scan in key frames to get list of angles
	i = f_start
	while i <= f_fall:
		vid[i].copy()

		b = getBall(vid[i], vid[i - 1], i + 1)

		cv2.circle(orgVid[i], (int(b[0]), int(b[1])), 5, (100, 255, 50), -1)

		cv2.imshow("Display", orgVid[i])
		cv2.waitKey(1)  # frame rate

		i = i + 1

	print("fall angle: ", angles[-1:][0])
	write(angles, arrFileOut)


# getAngles()
