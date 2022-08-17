from src import scanAngs
from vars import *
import setupVideo
import runMapping

def pos2angs(ball_positions):
	return [setupVideo.getAngle(x) for x in ball_positions]


# take out error angles in array from reading, replace errors with -1 to maintain frame count
def cleanAngs(ball_angs):

	CW = directionIsClockwise(ball_angs)

	for i in range(len(ball_angs)-1):
		if CW and ball_angs[i] > ball_angs[i + 1]:
			ball_angs[i] = -1

	return ball_angs


def cleanVels(ball_vels):
	out_vels = []
	last_vel = 0
	for i in range(len(ball_vels)-1)[::-1]:
		if ball_vels[i] > last_vel:
			out_vels.append(ball_vels[i])
			last_vel = ball_vels[i]
		else:
			out_vels.append(last_vel)

	if len(out_vels) < 2:
		return [0]
	return out_vels


def directionIsClockwise(ball_angs):

	ball_angs = [x for x in ball_angs if x != -1]

	if len(ball_angs) < 2:
		return True

	CWCount = 0
	CCWCount = 0
	maxContourArc = 180
	i = 0
	while i < len(ball_angs) - 1:
		# if ball is at the pole, reverse output
		if abs(ball_angs[i] - ball_angs[i + 1]) > maxContourArc:
			if ball_angs[i] < ball_angs[i + 1]:
				CCWCount += 1
			if ball_angs[i] > ball_angs[i + 1]:
				CWCount += 1

		else:
			if ball_angs[i] < ball_angs[i + 1]:
				CWCount += 1
			else:
				CCWCount += 1

		i += 1

	if CWCount > CCWCount:
		return True
	else:
		return False


def getSpeedBySimpleAngChange(ball_positions):
	if len(ball_positions) < 2:
		return 0
	return runMapping.getVelocity(setupVideo.getAngle(ball_positions[-1]), setupVideo.getAngle(ball_positions[-2]))


def getSpeedByCleanedAngChange(ball_positions):
	return 0


def getSpeedByRevolutions(ball_positions):
	if len(ball_positions) < 2:
		return 0
	ball_angs = cleanAngs(pos2angs(ball_positions))
	return scanAngs.timeForRev2(ball_angs, ball_angs[-1])


def getSpeedByMappedVel(ball_positions):
	return 0


def getSpeedByContourWidth(ball_positions):
	return 0


def getSpeed(ball_positions):
	return getSpeedBySimpleAngChange(ball_positions)

