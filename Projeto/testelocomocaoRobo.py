# coding=utf-8
# Insert in a script in Coppelia
# simRemoteApi.start(19999)
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

import math
import time
import numpy as np

PRETO = 0
VERMELHO = 1
AMARELO = 2
VERDE = 3
AZUL = 5
BRANCO = 6
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
axisX = 0
axisY = 1

def PrintSim(mensagem):
    sim.simxAddStatusbarMessage(clientID, mensagem, sim.simx_opmode_oneshot_wait)

def TimeOut(dist, startTime):
    currenttime = time.time()
    #print(startTime, currenttime)
    if (currenttime - startTime > abs(dist*100 + 1)):
        return True
    return False

## FUNCOES DOS SENSORES ######################################


def getDistanceIR(sensor):
    max_distance_IR = 1
    erro = 1
    while (erro != 0): 
        erro, detectable, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(clientID, sensor, sim.simx_opmode_streaming)
    #print(erro, detectable, distancePoint, detectedObjectHandle, detectedSurface)
    distance = distancePoint[2]
    if(detectable == False):
        distance = max_distance_IR
    #print(distance)
    return distance

def getColor(sensor):
    min_color_value = 200
    erro , resolution , Image = sim.simxGetVisionSensorImage(clientID, color_sensor_Left, 0, sim.simx_opmode_buffer)
    while (erro != 0):
        erro , resolution , Image = sim.simxGetVisionSensorImage(clientID, color_sensor_Left, 0, sim.simx_opmode_buffer)
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
    


## FUNÇÕES DE LOCOMOÇAO ######################################

def MoveForward():
    vref = 1
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)


def MoveForwardPosition(dist):
    raio = 0.003735
    angref = dist/raio
    erro, angLeft = sim.simxGetJointPosition(clientID, robotLeftMotor, sim.simx_opmode_buffer)
    #print(erro, angLeft)
    erro, angRight = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_buffer)
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetPosition(clientID, robotLeftMotor, angref + angLeft, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(clientID, robotRightMotor, angref + angRight, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    #time.sleep(0.1)
    actualAngL = 0
    actualAngR = 0
    startTime = time.time()
    while ((int(actualAngL*1000) != int((angref + angLeft)*1000)) and (int(actualAngR*1000) != int((angref + angRight)*1000)  )):
        #print(actualAngR, angref + angRight)
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetPosition(clientID, robotLeftMotor, angref + angLeft, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetPosition(clientID, robotRightMotor, angref + angRight, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)
        erro, actualAngR = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_buffer)
        erro, actualAngL = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_buffer)
        if(TimeOut(dist, startTime)):
            print('timeout')
            break
    print(int(actualAngR*1000), int((angref + angRight)*1000))
        

def MoveBackward():
    vref = 1
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, -vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, -vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def Stop():
    vref=0
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def TurnRight():
    vref=1
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, -vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def Align():
    while (getColor(color_sensor_Left) != PRETO or getColor(color_sensor_Right) != PRETO):
        MoveForwardPosition(0.001)
    while (getColor(color_sensor_Left) != PRETO and getColor(color_sensor_Right)):
        if(getColor(color_sensor_Left) != PRETO):
            #Mover so roda esquerda
            MoveForwardPosition(0.001)
        if(getColor(color_sensor_Right) != PRETO):
            #Mover so roda direita
            MoveForwardPosition(0.001)

def MoveSquareForward():
    #MoveForwardPosition(0.027)
    #Align()
    print('foward')

def TurnInSquare(angle): #gira no centro do quadrado e vai para ponta
    print(angle)
    
def arrived(currentPosition, finalPosition): #Define se chegou ao local
    if(currentPosition == finalPosition):
        return True
    stockLocals = [32, 33, 35, 36, 42, 43, 45, 46]
    if(finalPosition in stockLocals): #O destino final não é o quadrante em si, mas um em volta dele
        minDistance = abs(finalPosition - currentPosition)
        if(minDistance == 1 or minDistance == 10): #checa se está a um quadrado de distância apenas
            return True
    return False


def correctDirection(myDirection, movement, axis): #define se o robô está virado para a direção correta, se não, corrige. Retorna direção atual
    if(axis == axisX):
        if(movement > 0): #Quer ir pra baixo (SUL)
            if(myDirection == SOUTH):
                return SOUTH
            else:
                if(myDirection == NORTH):
                    TurnInSquare(180)
                if(myDirection == WEST):
                    TurnInSquare(90)
                if(myDirection == EAST):
                    TurnInSquare(-90)
                return SOUTH
        if(movement < 0): #Quer ir pra cima (NORTE)
            if(myDirection == NORTH):
                return NORTH
            else:
                if(myDirection == SOUTH):
                    TurnInSquare(180)
                if(myDirection == WEST):
                    TurnInSquare(-90)
                if(myDirection == EAST):
                    TurnInSquare(90)
                return NORTH

    if(axis == axisY):
        if(movement > 0): #Quer ir pra direita (LESTE)
            if(myDirection == EAST):
                return EAST
            else:
                if(myDirection == WEST):
                    TurnInSquare(180)
                if(myDirection == NORTH):
                    TurnInSquare(-90)
                if(myDirection == SOUTH):
                    TurnInSquare(90)
                return EAST
        if(movement < 0): #Quer ir pra direita (OESTE)
            if(myDirection == WEST):
                return WEST
            else:
                if(myDirection == EAST):
                    TurnInSquare(180)
                if(myDirection == NORTH):
                    TurnInSquare(90)
                if(myDirection == SOUTH):
                    TurnInSquare(-90)
                return WEST

def notStockLocal(currentPosition, movement, axis): #define se o robô está em volta de uma aŕea de carga onde não pode entrar
    if(axis == axisX):
        if(movement > 0): #Quer ir pra baixo (SUL)
            cantBe = [22, 23, 25, 26] #Lista de lugares que não podem ir pra baixo por conta do local de carga
        if(movement < 0): #Quer ir pra cima (NORTE)
            cantBe = [52, 53, 55, 56]
    if(axis == axisY):
        if(movement > 0): #Quer ir pra direita (LESTE)
            cantBe = [31, 41, 34, 44]
        if(movement < 0): #Quer ir pra esquerda (OESTE)
            cantBe = [34, 44, 37, 47]
    if(currentPosition in cantBe):
        return False
    return True

def goAround(currentPosition, myDirection): #desvia da área de carga e retorna nova posição e direção
    if(currentPosition == 22):
        myDirection = correctDirection(myDirection, -1, axisY)
        MoveSquareForward()
        myDirection = correctDirection(myDirection, +1, axisX)
        MoveSquareForward()
        currentPosition = 31
    return currentPosition, myDirection


def goFromTo(currentPosition, finalPosition, myDirection):
    while(not arrived(currentPosition, finalPosition)):
        moveX = (finalPosition/10) - (currentPosition/10)
        moveY =  (finalPosition%10) - (currentPosition%10)
        if(moveY != 0 and notStockLocal(currentPosition, moveY, axisY)):
            myDirection = correctDirection(myDirection, moveY, axisY)
            MoveSquareForward()
            if(moveY > 0): #robô andou para a direita
                currentPosition += 1
            else: #robô andou para a esquerda
                currentPosition -= 1
        elif(moveX != 0 and notStockLocal(currentPosition, moveX, axisX)):
            myDirection = correctDirection(myDirection, moveX, axisX)
            MoveSquareForward()
            if(moveX > 0): #robô andou para baixo
                currentPosition += 10
            else:  #robô andou para cima
                currentPosition -= 10
        elif (moveY == 0 and not notStockLocal(currentPosition, moveX, axisX)): #o robô ja chegou no eixo Y, mas não pode se movimentar em X por conta da área de carga
            currentPosition, myDirection = goAround(currentPosition, myDirection)
        print(currentPosition)
        time.sleep(1)
        
            


##########################################

goFromTo(13, 62, SOUTH)
 
# print ('Program started')
# sim.simxFinish(-1) # just in case, close all opened connections
# clientID = sim.simxStart('127.0.0.1',19999,True,True,5000,5)
# robotname = 'Robot'
# #targetname = 'Target1'
# if clientID != -1:
#     sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
#     print ('Connected to remote API server')
#     sim.simxAddStatusbarMessage(clientID,'Funcionando...',sim.simx_opmode_oneshot_wait)
#     time.sleep(0.02)

#     # Coletar handles
#     #Robô
#     erro, robot = sim.simxGetObjectHandle(clientID, robotname, sim.simx_opmode_oneshot_wait) 
#     #Motores
#     [erro, robotLeftMotor] = sim.simxGetObjectHandle(clientID, 'Revolute_joint2',sim.simx_opmode_oneshot_wait)
#     [erro, robotRightMotor] = sim.simxGetObjectHandle(clientID, 'Revolute_joint1', sim.simx_opmode_oneshot_wait)
#     #Sensores
#     erro, irRight = sim.simxGetObjectHandle(clientID, 'Sensor_IR_direito', sim.simx_opmode_oneshot_wait)
#     erro, irLeft = sim.simxGetObjectHandle(clientID, 'Sensor_IR_esquerdo', sim.simx_opmode_oneshot_wait)
#     erro , color_sensor_Left = sim.simxGetObjectHandle(clientID, 'Sensor_cor_esquerda', sim.simx_opmode_blocking)
#     erro , color_sensor_Right = sim.simxGetObjectHandle(clientID, 'Sensor_cor_direita', sim.simx_opmode_blocking)
    

#     # Criar stream de dados
#     [erro, positionrobot] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_streaming)
#     #[erro, positiontarget] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_streaming)
#     erro, angLeft = sim.simxGetJointPosition(clientID, robotLeftMotor, sim.simx_opmode_streaming)
#     erro, angRight = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_streaming)
#     [erro, orientationrobot] = sim.simxGetObjectOrientation(clientID,robot,-1,sim.simx_opmode_streaming)
#     sim.simxReadProximitySensor(clientID, irRight, sim.simx_opmode_streaming)
#     sim.simxReadProximitySensor(clientID, irLeft, sim.simx_opmode_streaming)
#     sim.simxGetVisionSensorImage(clientID, color_sensor_Left, 0, sim.simx_opmode_streaming)
#     sim.simxGetVisionSensorImage(clientID, color_sensor_Right, 0, sim.simx_opmode_streaming)

#     time.sleep(2)

#     # # Comandos motores
#     # PrintSim('comecei')
#     # i = 0
#     # while (i < 5):
#     #     MoveForwardPosition(0.002)
#     #     i += 1
#     # #PrintSim('terminei')
#     # #time.sleep(5)
#     # MoveForwardPosition(0.0015)
#     # #time.sleep(2)
#     #
#     #Comando Sensores
#     for i in range(2):
#         MoveSquareForward()

#     cont = 0
#     while(cont < 100):
#         cont+=1
#         # Coletar dados robôs e alvos
#         [erro, [xr,yr,zr]] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_buffer)
#         #[erro, [xt,yt,zt]] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_buffer)
#         [erro, [alpha, beta, gamma]] = sim.simxGetObjectOrientation(clientID, robot, -1, sim.simx_opmode_buffer)

        
#         #sim.simxAddStatusbarMessage(clientID, 'A posição em x é '+str(xr) + ' e a posição em y é '+str(yr), sim.simx_opmode_oneshot_wait)

        

#     # Stop simulation:
#     # sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot_wait)

#     # Pause simulation
#     sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

#     # Now close the connection to V-REP:
#     sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking )
#     sim.simxFinish(clientID)
# else:
#     print ('Failed connecting to remote API server')
# print ('Program ended')




