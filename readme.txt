A project to track and predict where a ball in Roulette will fall. 
Given a video in, it uses OpenCv to track the ball, which predicts the velocity, which can then be mapped to an expected fall location. 

how to use:
-use setupVideo.getKeyFrames() to get the key frames [start,fall,stop]
-use setupVideo.getAngles to get an out mapping arr of all the angles recorded in the spin between key frames
-use scanAngs.scanAngles() to get the out velocities arr of all the velocities
-use scanAngs.mapVelToAngles() to get the out mapping arr from velocities which is the 'if its going this fast, it will fall +/- x degrees'
-use runMapping.getFallPoint() to get the fall point of the ball based on its velocities and the recorded mappings

-on display top is 180 deg, bottom is 0, left is 270-- mby fixed
-velocity is in frames per second

ideas:
-redo fall point calculation
-cant easily get the mid point between mappings because are working with angle midpoints
-adjust angles to be common sense
-adjust velocity to be more understandable
