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


def getPoint(angle):

	# angle = (angle+180) % 360

	length = 200
	c_x = center[0]
	c_y = center[1]

	x = round(c_x + length * math.sin(angle * math.pi / 180.0))
	y = round(c_y + length * math.cos(angle * math.pi / 180.0))

	P2 = (x, y)

	return P2


def getVelocity(ang, last_ang):
	# get distance between angles
	dif = ((((ang - last_ang) % 360) + 540) % 360) - 180

	# 360 / diff = frames for revolution?? may show diff speed than scan arr produces
	# (int)*100 for accuracy used
	if dif == 0: return 0
	vel = int((360 / dif) * 100)

	return vel


def read(readFile):
	arr = []
	with open(path + readFile, 'r') as fd:
		for row in fd:
			lines = row.split(',')
			lines = lines[0:-1]
			lines = [(x[1:-1]) for x in lines]
			arr = arr + lines

	mapping2d = []
	for x in arr:
		y = x.split('=')
		if len(y) == 2:
			z = [0, 0]
			z[0] = int(y[0])
			z[1] = float(y[1])
			mapping2d.append(z)
		mapping2d.sort()
	# print(mapping2d)

	return mapping2d


mapping = read(mapFileOut)


def getExpectedFromMap(vel):

	for x in mapping:
		if x[0] > vel:
			return x[1]
	return 0


def getAverageAngle(arr):
	x = y = 0
	for angle in arr:
		angle = math.radians(angle)
		x += math.cos(angle)
		y += math.sin(angle)

	average_angle = math.degrees(math.atan2(y, x)) % 360

	return average_angle


def getFallPoint():
	print("guessing on: " + fileIn)

	get_frames()

	fall_points = []
	last_ang = 0
	i_max = len(orgVid)
	i = 0

	f_start = KeyVals[START]
	f_fall = KeyVals[FALL]

	# for each frame
	j = 1
	i = f_start
	while i <= f_fall:

		# get ball
		vid[i].copy()

		b = getBall(vid[i], vid[i - 1], i + 1)
		cv2.circle(orgVid[i], (int(b[0]), int(b[1])), 5, (100, 255, 50), -1)

		# get angle
		ang = getAngle(b)

		if ang == -1:
			j += 1
			print("skip frame: ", i)
		else:

			# get vel = diff from last angle
			vel = getVelocity(ang, last_ang) / j
			last_ang = ang

			# get expected landing = mapping: angle + difference
			fall_point_frame = getExpectedFromMap(vel)
			fall_points.append(fall_point_frame)

			# draw calculated landing for frame
			# print("frame ", i, " guess: ", fall_point_frame)
			# draw average guess

			j = 1

		averageAngle = getAverageAngle(fall_points)
		# print("average guess: ", averageAngle)

		cv2.circle(orgVid[i], getPoint(averageAngle), 3, (100, 20, 50), -1)
		cv2.imshow("Display", orgVid[i])
		cv2.waitKey(30)  # frame rate

		i += 1


getFallPoint()

