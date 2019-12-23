#Импорт библиотек
import time
import numpy as np
import matplotlib.pyplot as plt #Библиотека визуализации графики
import vrep #Библиотека виртуальной среды
import random
from skimage import color, measure, draw #Библиотека анализа изображений

print ('Program started')
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID!=-1:
    print ('Connected to remote API server')
    vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)

    #Получение изображений с камер
    error, camera_1 = vrep.simxGetObjectHandle(clientID, 'perspective_vision_1', vrep.simx_opmode_oneshot_wait) #Левая камера
    error, camera_2 = vrep.simxGetObjectHandle(clientID, 'perspective_vision_2', vrep.simx_opmode_oneshot_wait) #Правая камера
    
    error, resolution, image_1 = vrep.simxGetVisionSensorImage(clientID, camera_1, 0, vrep.simx_opmode_streaming)
    error, resolution, image_2 = vrep.simxGetVisionSensorImage(clientID, camera_2, 0, vrep.simx_opmode_streaming)

    time.sleep(0.1)
    increment = 0
    message = 0

    error, info = vrep.simxGetInMessageInfo(clientID, vrep.simx_headeroffset_server_state) #Состояние подключения
    while (info != 0):
        error, resolution, image_1 = vrep.simxGetVisionSensorImage(clientID, camera_1, 0, vrep.simx_opmode_buffer)
        error, resolution, image_2 = vrep.simxGetVisionSensorImage(clientID, camera_2, 0, vrep.simx_opmode_buffer)
        if error == vrep.simx_return_ok:
            if increment <= 200: #Пока снимков меньше 200            
                img_1 = np.array(image_1, dtype = np.uint8)
                img_1.resize([resolution[1], resolution[0],3])
                img_1 = np.flip(img_1, axis=0) #Отразить полученное изображение по вертикали

                plt.imsave("D:/robot_workspace/photos/textured/fig_{}.png".format(increment), img_1) #Запись в файл

                img_2 = np.array(image_2, dtype = np.uint8)
                img_2.resize([resolution[1], resolution[0],3])
                img_2 = np.flip(img_2, axis=0)

                plt.imsave("D:/robot_workspace/photos/discoloured/fig_{}.png".format(increment), img_2)

                increment += 1

                time.sleep(0.25) #Период создания снимков
            else:
                if message == 0:
                    print ('Max count of images')
                    message = 1
        else:
            print('Error:', error)

        error, info = vrep.simxGetInMessageInfo(clientID, vrep.simx_headeroffset_server_state)

    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')