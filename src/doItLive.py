import setupVideo
from vars import *

def print_balls(ball_positions, frame):

	cv2.circle(orgVid[frame], (int(ball_positions[-1][0]), int(ball_positions[-1][1])), 5, (100, 100, 255), -1)

	num_of_balls = 5
	decrase = 255 / num_of_balls
	g = b = 0
	for ball in ball_positions[-num_of_balls:-1]:
		g = g + decrase
		b = b + decrase
		cv2.circle(orgVid[frame], (int(ball[0]), int(ball[1])), 5, (0, g, b), -1)

# get the list of angles of the ball for the scanned video
def runLive():

	#load video
	setupVideo.get_frames()

	# load key frames
	f_start = KeyVals[START]
	f_fall = KeyVals[FALL]

	ball_positions = []

	# scan in key frames to get list of angles
	i = f_start
	while i <= f_fall:

		vid[i].copy()

		#get current ball location
		ball_positions.append(setupVideo.getBall(vid[i], vid[i - 1], i + 1))

		print_balls(ball_positions, i)
		cv2.imshow("Display", orgVid[i])
		cv2.waitKey(100)  # frame rate

		i = i + 1


runLive()
