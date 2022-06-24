import setupVideo
from vars import *

# get the list of angles of the ball for the scanned video
def runLive():

	#load video
	setupVideo.get_frames()

	# load key frames
	f_start = KeyVals[START]
	f_fall = KeyVals[FALL]

	# scan in key frames to get list of angles
	i = f_start
	ball_last1 =(0,0)
	ball_last2 =(0,0)
	ball_last3 =(0,0)
	ball_last4 =(0,0)
	ball_last5 =(0,0)
	while i <= f_fall:
		vid[i].copy()

		#get and draw current ball location
		ball = setupVideo.getBall(vid[i], vid[i - 1], i + 1)
		cv2.circle(orgVid[i], (int(ball[0]), int(ball[1])), 5, (100, 100, 255), -1)
		cv2.circle(orgVid[i], (int(ball_last1[0]), int(ball_last1[1])), 5, (0, 255, 150), -1)
		cv2.circle(orgVid[i], (int(ball_last2[0]), int(ball_last2[1])), 5, (0, 200, 100), -1)
		cv2.circle(orgVid[i], (int(ball_last3[0]), int(ball_last3[1])), 5, (0, 150, 75), -1)
		cv2.circle(orgVid[i], (int(ball_last4[0]), int(ball_last4[1])), 5, (0, 100, 50), -1)
		cv2.circle(orgVid[i], (int(ball_last5[0]), int(ball_last5[1])), 5, (0, 50, 25), -1)
		ball_last5 = ball_last4
		ball_last4 = ball_last3
		ball_last3 = ball_last2
		ball_last2 = ball_last1
		ball_last1 = ball

		cv2.imshow("Display", orgVid[i])
		cv2.waitKey(300)  # frame rate

		i = i + 1


runLive()