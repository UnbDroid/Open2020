# coding=utf-8
# Insert in a script in Coppelia

import sim
import numpy as np
import globalDefs as glob
from globalDefs import *

## FUNCOES DOS SENSORES ######################################


def getDistanceIR(sensor):
    max_distance_IR = 1
    erro = 1
    while (erro != 0): 
        erro, detectable, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(glob.clientID, sensor, sim.simx_opmode_streaming)
    #print(erro, detectable, distancePoint, detectedObjectHandle, detectedSurface)
    distance = distancePoint[2]
    if(detectable == False):
        distance = max_distance_IR
    #print(distance)
    return distance

def getCubeHandle(sensor):
    erro = 1
    while (erro != 0): 
        erro, detectable, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(glob.clientID, sensor, sim.simx_opmode_streaming)
    return detectedObjectHandle

def getColor(sensor):
    min_color_value = 200
    erro , resolution , Image = sim.simxGetVisionSensorImage(glob.clientID, sensor, 0, sim.simx_opmode_buffer)
    while (erro != 0):
        erro , resolution , Image = sim.simxGetVisionSensorImage(glob.clientID, sensor, 0, sim.simx_opmode_buffer)
    img = np.array(Image,dtype=np.uint8)
    #print(resolution, img)
    rgb_color = 0
    if (img[0] > min_color_value): 
        rgb_color += 100
    if (img[1] > min_color_value): 
        rgb_color += 10
    if (img[2] > min_color_value): 
        rgb_color += 1
    if (rgb_color == 1):
        return AZUL
    if (rgb_color == 10):
        return VERDE
    if (rgb_color == 100):
        return VERMELHO
    if (rgb_color == 110):
        return AMARELO
    if (rgb_color == 111):
        return BRANCO
    return PRETO