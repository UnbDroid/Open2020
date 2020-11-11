# coding=utf-8
# Insert in a script in Coppelia

import sim
import globalDefs as glob
from globalDefs import *
import time

## FUNÇÕES DA GARRA ##########################################

def subir_elevador(altura):
    sim.simxSetJointTargetPosition(glob.clientID,glob.elevador,altura,sim.simx_opmode_oneshot) 
    time.sleep(1)

def descer_elevador():
    sim.simxSetJointTargetPosition(glob.clientID,glob.elevador,-0.15,sim.simx_opmode_oneshot)
    time.sleep(1)

def abrir_garra():
    sim.simxPauseCommunication(glob.clientID, True)
    sim.simxSetJointTargetPosition(glob.clientID,glob.paDireita,0.04,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(glob.clientID,glob.paEsquerda,0.04,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(glob.clientID, False)
    time.sleep(1.5)

def fechar_garra(): 
    sim.simxPauseCommunication(glob.clientID, True)
    sim.simxSetJointTargetPosition(glob.clientID,glob.paDireita,0.025,sim.simx_opmode_oneshot) 
    sim.simxSetJointTargetPosition(glob.clientID,glob.paEsquerda,0.025,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(glob.clientID, False)
    time.sleep(1)

def fechar_garra_total():
    sim.simxPauseCommunication(glob.clientID, True)
    sim.simxSetJointTargetPosition(glob.clientID,glob.paDireita, 0.015, sim.simx_opmode_oneshot) 
    sim.simxSetJointTargetPosition(glob.clientID,glob.paEsquerda, 0.015, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(glob.clientID, False)
    time.sleep(1)

def fechar_garra_cubo(cube):
    erro = 1
    # while erro != 0:
    #     erro, robotPosition = sim.simxGetObjectPosition(glob.clientID, glob.robo, -1, sim.simx_opmode_streaming)
    # erro = 1
    while erro != 0:
        erro, cubePosition = sim.simxGetObjectPosition(glob.clientID, cube, glob.robo, sim.simx_opmode_streaming)
    #print(robotPosition)
    #print(cubePosition)
    cubePosition[0] = 0
    erro = 1
    while erro != 0:
        sim.simxPauseCommunication(glob.clientID, True)
        sim.simxSetJointTargetPosition(glob.clientID,glob.paDireita,0.025,sim.simx_opmode_oneshot) 
        sim.simxSetJointTargetPosition(glob.clientID,glob.paEsquerda,0.025,sim.simx_opmode_oneshot)
        erro = sim.simxSetObjectPosition(glob.clientID, cube, glob.robo, cubePosition, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(glob.clientID, False)
    time.sleep(1)
