from utility.vrep import vrep
import time
import numpy as np 
from skimage import color, measure
import matplotlib.pyplot as plt

print ('Program started')
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
if clientID!=-1:
    print ('Connected to remote API server')
    vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)

    error, cameraBrick = vrep.simxGetObjectHandle(clientID, 'camBrick', vrep.simx_opmode_oneshot_wait)
    error, cameraWhite = vrep.simxGetObjectHandle(clientID, 'camWhite', vrep.simx_opmode_oneshot_wait)
    error, resolution, imageBrick = vrep.simxGetVisionSensorImage(clientID, cameraBrick, 0,vrep.simx_opmode_streaming)
    error, resolution, imageWhite = vrep.simxGetVisionSensorImage(clientID, cameraWhite, 0,vrep.simx_opmode_streaming)
    time.sleep(0.3)

    for i in range(150):
        vrep.simxPauseSimulation(clientID, vrep.simx_opmode_oneshot)
        time.sleep(0.5)

        error, resolution, imageBrick = vrep.simxGetVisionSensorImage(clientID, cameraBrick, 0,vrep.simx_opmode_buffer)
        error, resolution, imageWhite = vrep.simxGetVisionSensorImage(clientID, cameraWhite, 0,vrep.simx_opmode_buffer)

        if error == vrep.simx_return_ok:
            imgBrick = np.array(imageBrick, dtype=np.uint8)
            imgWhite = np.array(imageWhite, dtype=np.uint8)
            imgBrick.resize([resolution[1],resolution[0],3])
            imgWhite.resize([resolution[1],resolution[0],3])

            plt.imsave('E:/Images/Bricks/brick{}.png'.format(i), imgBrick)
            plt.imsave('E:/Images/White/white{}.png'.format(i), imgWhite)
        else:
            print('Error:', error)

        vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)
        time.sleep(0.5)

    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
    time.sleep(1)
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')