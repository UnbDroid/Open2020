# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
	import sim
except:
	print ('--------------------------------------------------------------')
	print ('"sim.py" could not be imported. This means very probably that')
	print ('either "sim.py" or the remoteApi library could not be found.')
	print ('Make sure both are in the same folder as this file,')
	print ('or appropriately adjust the file "sim.py"')
	print ('--------------------------------------------------------------')
	print ('')

import time
import visionAlgo as vis
import firstSq as one
# START

print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19998,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:
	print ('Connected to remote API server')
	time.sleep(2)

	#result = vis.resolveVision(clientID,0)
	#result = vis.getNumber(clientID)
	result = vis.getCode(clientID)
	#print(one.identifyFirstPos(clientID))
	#print(result)

	# Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
	sim.simxGetPingTime(clientID)

	# Now close the connection to CoppeliaSim:
	sim.simxFinish(clientID)
else:
	print ('Failed connecting to remote API server')
print ('Program ended')