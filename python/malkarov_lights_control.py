#Импорт библиотек
import time
import numpy as np
import matplotlib.pyplot as plt #Библиотека визуализации графики
import vrep #Библиотека виртуальной среды
from skimage import color, measure #Библиотека анализа изображений

#Вывод информации о запуске программы
print ('Program started')

#Подключение к удалённой сессии
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID!=-1:
    #Если подключение произошло успешно...
    print ('Connected to remote API server')
    vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)

    #Подключение двигателей и камеры
    error, motor_left = vrep.simxGetObjectHandle(clientID, 'nakedCar_motorLeft', vrep.simx_opmode_oneshot_wait)
    error, motor_right = vrep.simxGetObjectHandle(clientID, 'nakedCar_motorRight', vrep.simx_opmode_oneshot_wait)
    error, camera = vrep.simxGetObjectHandle(clientID, 'perspective_vision', vrep.simx_opmode_oneshot_wait)
    
    #Подключение камеры
    error, resolution, image = vrep.simxGetVisionSensorImage(clientID, camera, 0, vrep.simx_opmode_streaming)

    #Установка задержки 0.1 секунды
    time.sleep(0.1)

    #Состояние подключения к виртуальной сессии
    error, info = vrep.simxGetInMessageInfo(clientID, vrep.simx_headeroffset_server_state)

    #Пока нет ошибки...
    while (info != 0):
        error, resolution, image = vrep.simxGetVisionSensorImage(clientID, camera, 0, vrep.simx_opmode_buffer) #Полчение изображения
        
        #Если нет ошибки чтения изображения, приступить к чтению данных с камеры...
        if error == vrep.simx_return_ok:

            #Получение массива из изображения
            img = np.array(image, dtype = np.uint8)
            img.resize([resolution[1], resolution[0],3])
            img_h = color.rgb2hsv(img)[...,0]
            img_s = color.rgb2hsv(img)[...,1]

            #Установка цветовых диапазонов
            red_range = (img_h < 0.15) & (img_s > 0.5) #Красный
            yellow_range = (img_h > 0.15) & (img_h < 0.2) & (img_s > 0.5) #Жёлтый
            green_range = (img_h > 0.2) & (img_h < 0.4) & (img_s > 0.5) #Зелёный

            #Обработка красного сигнала
            red = measure.label(red_range)
            red = measure.regionprops(red)

            #Если обработанный цвет – красный...
            if len(red) != 0:

                #Если размер обекта больше 5%...
                if red[0].area/red_range.size > 0.05:

                    #Записать нулевую скорость двигателям
                    error = vrep.simxSetJointTargetVelocity(clientID, motor_left, 0, vrep.simx_opmode_oneshot)
                    error = vrep.simxSetJointTargetVelocity(clientID, motor_right, 0, vrep.simx_opmode_oneshot)
            
            #Обработка жёлтого сигнала
            yellow = measure.label(yellow_range)
            yellow = measure.regionprops(yellow)

            #Если обработанный цвет – жёлтый...
            if len(yellow) != 0:

                #Если размер обекта больше 5%...
                if yellow[0].area/yellow_range.size > 0.05:

                    #Записать скорость двигателям, равную 1
                    error = vrep.simxSetJointTargetVelocity(clientID, motor_left, 1, vrep.simx_opmode_oneshot)
                    error = vrep.simxSetJointTargetVelocity(clientID, motor_right, 1, vrep.simx_opmode_oneshot)

            #Обработка зелёного сигнала
            green = measure.label(green_range)
            green = measure.regionprops(green)
            
            #Если обработанный цвет – зелёный...
            if len(green) != 0:

                #Если размер обекта больше 5%...
                if green[0].area/green_range.size>0.05:

                    #Записать скорость двигателям, равную 3
                    error=vrep.simxSetJointTargetVelocity(clientID, motor_left, 3, vrep.simx_opmode_oneshot)
                    error=vrep.simxSetJointTargetVelocity(clientID, motor_right, 3, vrep.simx_opmode_oneshot)

        else:
            print('Error:', error) #Вывести, если возникла ошибка чтения

        error, info = vrep.simxGetInMessageInfo(clientID, vrep.simx_headeroffset_server_state)

    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server') #Вывести, если возникла ошибка подключения
print ('Program ended') #Вывести при завершении приложения