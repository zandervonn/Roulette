import numpy

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

		numpy.set_printoptions(threshold=np.inf)  # to not truncate array
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


def get_clockwise_point(contour):
	t_p = (0, 0)
	t_a = 360
	maxContourArc = 180

	# get list of angles in contour
	cont_angs = []
	for x in contour:
		point = x[0]
		cont_angs.append(getAngle(point))

	# if angles are at both sides of 360, you are at the top of the circle
	top = False
	sorted_angs = sorted(cont_angs)
	if len(sorted_angs) > 0 and sorted_angs[0] < 360-maxContourArc and sorted_angs[-1] > 0+maxContourArc:
		top = True

	# for all points in contour
	for x in contour:
		point = x[0]
		a = getAngle(point)
		# if ball at top get only clockwise points
		if top and maxContourArc < a < t_a:
			t_p = point
			t_a = a
		# otherwise check all points
		elif not top and a < t_a:
			t_p = point
			t_a = a

	# if t_p value is invalid
	if not t_p[1] > 0:
		t_p = (0, 0)
		t_a = 360

	return t_a, t_p


def getBall(tmp, last):

	subbed = tmp
	height, width, z = tmp.shape
	inner = int(height * 0.435)

	# fill inner circle
	subbed = cv2.circle(subbed, center, inner, (0, 0, 0), -1)
	subbed = cv2.subtract(subbed, last)  # get change between frames (moving)

	# convert to grey, blue to get bigger items, get the brightest point
	subbed = cv2.cvtColor(subbed, cv2.COLOR_RGB2GRAY)
	subbed = cv2.GaussianBlur(subbed, (21, 21), 0)
	limit = subbed.max()

	# rangeT from the brightest point that may be the ball
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

	contour = []
	if len(contours) != 0:
		# find the biggest contour (c) by the area
		contour = max(contours, key=cv2.contourArea)

	t_a, t_p = get_clockwise_point(contour)

	# get farthest clockwise point in contour = t _ a
	if contour is not None and len(contour) > 1:
		t_a, t_q = get_clockwise_point(contour)
		angles.append(t_a)

	return t_p


# scan the video for key frames
# a = backward
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

		b = getBall(vid[i], vid[i - 1])

		cv2.circle(orgVid[i], (int(b[0]), int(b[1])), 5, (100, 255, 50), -1)

		cv2.imshow("Display", orgVid[i])
		cv2.waitKey(1)  # frame rate

		i = i + 1

	print("fall angle: ", angles[-1:][0])
	write(angles, arrFileOut)


# get_frames()
