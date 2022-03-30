how to use:
-use setupVideo.getKeyFrames() to get the key frames [start,fall,stop]
-use setupVideo.getAngles to get an out mapping arr of all the angles recorded in the spin between key frames
-use scanAngs.scanAngles() to get the out velocities arr of all the velocities
-use scanAngs.mapVelToAngles() to get the out mapping arr from velocities which is the 'if its going this fast, it will fall +/- x degrees'
-use runMapping.getFallPoint() to get the fall point of the ball based on its velocities and the recorded mappings


ideas: