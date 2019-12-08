import vrep
import time
import numpy as np
from skimage import draw, measure, data, color
import matplotlib.pyplot as plt

print ('Program started')
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
if clientID!=-1:
    print ('Connected to remote API server')
    error, camera = vrep.simxGetObjectHandle(clientID, 'v0', vrep.simx_opmode_oneshot_wait)
    error, car = vrep.simxGetObjectHandle(clientID, 'nakedAckermannSteeringCar', vrep.simx_opmode_oneshot_wait)
    error, motor_left = vrep.simxGetObjectHandle(clientID, 'nakedCar_motorLeft', vrep.simx_opmode_oneshot_wait)
    error, motor_right = vrep.simxGetObjectHandle(clientID, 'nakedCar_motorRight', vrep.simx_opmode_oneshot_wait)
    error, resolution, image = vrep.simxGetVisionSensorImage(clientID, camera, 0,vrep.simx_opmode_streaming)

    time.sleep(0.1)
    while (vrep.simxGetConnectionId(clientID) != -1):
        error, resolution, image = vrep.simxGetVisionSensorImage(clientID, camera, 0,vrep.simx_opmode_buffer)
        if error == vrep.simx_return_ok:
            img = np.array(image, dtype=np.uint8)
            img.resize([resolution[1],resolution[0],3])
            imgH = color.rgb2hsv(img)[...,0]
            imgS = color.rgb2hsv(img)[...,1]
            red = (imgH<0.15) & (imgS>0.5)
            green = (imgH>0.2) & (imgH<0.4) & (imgS>0.5)
            
            redSignal = measure.label(red)
            redSignal = measure.regionprops(redSignal)
            if len(redSignal)!=0:
                if redSignal[0].area/red.size>0.05:
                    error = vrep.simxSetJointTargetVelocity(clientID, motor_left, 0, vrep.simx_opmode_oneshot)
                    error = vrep.simxSetJointTargetVelocity(clientID, motor_right, 0, vrep.simx_opmode_oneshot)

            greenSignal = measure.label(green)
            greenSignal = measure.regionprops(greenSignal)

            if len(greenSignal)!=0:
                if greenSignal[0].area/green.size>0.05:
                    error = vrep.simxSetJointTargetVelocity(clientID, motor_left, 10, vrep.simx_opmode_oneshot)
                    error = vrep.simxSetJointTargetVelocity(clientID, motor_right, 10, vrep.simx_opmode_oneshot)

        else:
            print('Error:', error)

        error, info = vrep.simxGetInMessageInfo(clientID, vrep.simx_headeroffset_server_state)

    vrep.simxFinish(clientID)

else:
    print ('Failed connecting to remote API server')
print ('Program ended')