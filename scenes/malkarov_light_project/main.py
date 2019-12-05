import sys
import os
import time
from utility.vrep import vrep

print("Program started")
vrep.simxFinish(-1)
clientID = vrep.simxStart("127.0.0.1", 19999, True, True, 5000, 5)
if clientID != -1:
    print("Connected to remote API server")
    vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
    res, objs = vrep.simxGetObjects(
        clientID, vrep.sim_handle_all, vrep.simx_opmode_blocking
    )
    if res == vrep.simx_return_ok:
        print("Number of objects in the scene: ", len(objs))
    else:
        print("Remote API function call returned with error code: ", res)
    time.sleep(2)

    #tt = vrep.simxGetStringSignal(clientID, "nt", vrep.simx_opmode_oneshot_wait) #simxGetStringSignal(clientId,"mySignalName",&signalValue,&signalLength,operationMode)==simx_return_ok:
    #print(tt)
    un = vrep.simxGetIntegerSignal(clientID, "nt", vrep.simx_opmode_oneshot_wait)
    print(un[1])

    vrep.simxFinish(clientID)
else:
    print("Failed connecting to remote API server")
print("Program ended")
