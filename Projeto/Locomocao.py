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

frente = 1
tras = -1
direita = 1
esquerda = -1


def PrintSim(mensagem):
    sim.simxAddStatusbarMessage(clientID, mensagem, sim.simx_opmode_oneshot_wait)


def TimeOutDist(dist, startTime):
    currenttime = time.time()
    # print(startTime, currenttime)
    if (currenttime - startTime > abs(dist * 100 + 1)):
        return True
    return False

def TimeOutAng(ang, startTime):
    currenttime = time.time()
    if (currenttime - startTime > abs(ang * 100 + 1)):
        return True
    return False


## FUNCOES DOS SENSORES ######################################


def getDistanceIR(sensor):
    max_distance_IR = 1
    erro = 1
    while (erro != 0):
        erro, detectable, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(clientID,
                                                                                                             sensor,
                                                                                                             sim.simx_opmode_streaming)
    # print(erro, detectable, distancePoint, detectedObjectHandle, detectedSurface)
    distance = distancePoint[2]
    if (detectable == False):
        distance = max_distance_IR
    # print(distance)
    return distance


def getColor(sensor):
    min_color_value = 200
    erro, resolution, Image = sim.simxGetVisionSensorImage(clientID, color_sensor_Left, 0, sim.simx_opmode_buffer)
    while (erro != 0):
        erro, resolution, Image = sim.simxGetVisionSensorImage(clientID, color_sensor_Left, 0, sim.simx_opmode_buffer)
    img = np.array(Image, dtype=np.uint8)
    # print(resolution, img)
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

def MoveBackward():
    vref = -1
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def MoveDirectionPosition(direcao, dist):   #Andar reto para frente ou para trás
    #direcao: 1 = frente, -1 = tras
    raio = 0.003735
    angref = direcao*dist / raio
    erro, angRight = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_buffer)
    erro, angLeft = sim.simxGetJointPosition(clientID, robotLeftMotor, sim.simx_opmode_buffer)
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetPosition(clientID, robotRightMotor, angref + angRight, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(clientID, robotLeftMotor, angref + angLeft, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    actualAngR = 0
    actualAngL = 0
    startTime = time.time()
    while ((int(actualAngR * 1000) != int((angref + angRight) * 1000)) and (
            int(actualAngL * 1000) != int((angref + angLeft) * 1000))):
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetPosition(clientID, robotRightMotor, angref + angRight, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetPosition(clientID, robotLeftMotor, angref + angLeft, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)
        erro, actualAngR = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_buffer)
        erro, actualAngL = sim.simxGetJointPosition(clientID, robotLeftMotor, sim.simx_opmode_buffer)
        if (TimeOutDist(dist, startTime)):
            print('timeout')
            break
    print(int(actualAngR * 1000), int((angref + angRight) * 1000))
    print(int(actualAngL * 1000), int((angref + angLeft) * 1000))

    #para melhorar: em vez de usar um chute para uma volta completa, calcular o perimetro do circulo centrado no robo
    #e de raio igual a distancia entre o centro e a roda, dividir esse valor pelo perimetro da roda e
    #usar a mesma conversao que a funcao de andar reto

def Stop():
    vref = 0
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def TurnRight():
    vref = 1
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, -vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def TurnLeft():
    vref = 1
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor,-vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def TurnDirectionAng(direcao, ang):   #Girar para a direita ou para a esquerda pelo angulo que você escolher
    #ang em graus
    #direcao: 1 = direita, -1 = esquerda
    angref = direcao*ang*(np.pi*180)*(0.04188/360)
    erro, angRight = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_buffer)
    erro, angLeft = sim.simxGetJointPosition(clientID, robotLeftMotor, sim.simx_opmode_buffer)
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetPosition(clientID, robotRightMotor, angref + angRight, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(clientID, robotLeftMotor, -angref + angLeft, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    actualAngR = 0
    actualAngL = 0
    startTime = time.time()
    while ((int(actualAngR * 1000) != int((angref + angRight) * 1000)) and (
            int(actualAngL * 1000) != int((-angref + angLeft) * 1000))):
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetPosition(clientID, robotRightMotor, angref + angRight, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetPosition(clientID, robotLeftMotor, -angref + angLeft, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)
        erro, actualAngR = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_buffer)
        erro, actualAngL = sim.simxGetJointPosition(clientID, robotLeftMotor, sim.simx_opmode_buffer)
        if (TimeOutAng(ang, startTime)):
            print('timeout')
            break
    print(int(actualAngR * 1000), int((angref + angRight) * 1000))
    print(int(actualAngL * 1000), int((-angref + angLeft) * 1000))


def Align():   #em desenvolvimento
    while(getColor(color_sensor_Left) != PRETO and getColor(color_sensor_Right) != PRETO):
        MoveDirectionPosition(tras, 0.001)
        print("To procurando a linha")
    print("Achei a linha")

    #while (getColor(color_sensor_Left) != PRETO or getColor(color_sensor_Right) != PRETO):
        #MoveDirectionPosition(1, 0.001)
        #Stop()
    if (getColor(color_sensor_Left != PRETO)):
        print("Esquerdo branco")
    else: #(getColor(color_sensor_Right) == PRETO):
        print("Esquerdo preto")
    if (getColor(color_sensor_Right != PRETO)):
        print("Direito branco")
    else: #(getColor(color_sensor_Left) == PRETO):
        print("Direito preto")

        #print("To procurando a linha")
        #while ((getColor(color_sensor_Left) != PRETO and getColor(color_sensor_Right) == PRETO) or (getColor(color_sensor_Left) == PRETO and getColor(color_sensor_Right) != PRETO)):
            #print("Achei a linha")
            #if (getColor(color_sensor_Left) != PRETO):
            # Mover so roda esquerda
                #print("Vamos girar")
                #TurnDirectionAng(direita, 1)
                #print("Girando para a direita")
            #MoveDirectionPosition(frente, 0.001)
            #elif (getColor(color_sensor_Right) != PRETO):
            # Mover so roda direita
                #TurnDirectionAng(esquerda, 1)
                #print("Girando para a esquerda")
            #MoveDirectionPosition(frente, 0.001)


def MoveDirectionSquare(direcao, n):   #Anda n quadrados pra frente ou pra trás
    #frente = 1, tras = -1
    i = 0
    while (i < n):
        MoveDirectionPosition(direcao, 0.027)
        i += 1
    Align()


def TurnInsideSquare(direcao, ang):   #em desenvolvimento
    Align()
    MoveDirectionPosition(tras, 0.0135)
    TurnDirectionAng(direcao, ang)



##########################################


print ('Program started')
sim.simxFinish(-1)  # just in case, close all opened connections
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
robotname = 'Robot'
# targetname = 'Target1'
if clientID != -1:
    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
    print ('Connected to remote API server')
    sim.simxAddStatusbarMessage(clientID, 'Funcionando...', sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)

    # Coletar handles
    # Robô
    erro, robot = sim.simxGetObjectHandle(clientID, robotname, sim.simx_opmode_oneshot_wait)
    # Motores
    [erro, robotLeftMotor] = sim.simxGetObjectHandle(clientID, 'Revolute_joint2', sim.simx_opmode_oneshot_wait)
    [erro, robotRightMotor] = sim.simxGetObjectHandle(clientID, 'Revolute_joint1', sim.simx_opmode_oneshot_wait)
    # Sensores
    erro, irRight = sim.simxGetObjectHandle(clientID, 'Sensor_IR_direito', sim.simx_opmode_oneshot_wait)
    erro, irLeft = sim.simxGetObjectHandle(clientID, 'Sensor_IR_esquerdo', sim.simx_opmode_oneshot_wait)
    erro, color_sensor_Left = sim.simxGetObjectHandle(clientID, 'Sensor_cor_esquerda', sim.simx_opmode_blocking)
    erro, color_sensor_Right = sim.simxGetObjectHandle(clientID, 'Sensor_cor_direita', sim.simx_opmode_blocking)

    # Criar stream de dados
    [erro, positionrobot] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_streaming)
    # [erro, positiontarget] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_streaming)
    erro, angLeft = sim.simxGetJointPosition(clientID, robotLeftMotor, sim.simx_opmode_streaming)
    erro, angRight = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_streaming)
    [erro, orientationrobot] = sim.simxGetObjectOrientation(clientID, robot, -1, sim.simx_opmode_streaming)
    sim.simxReadProximitySensor(clientID, irRight, sim.simx_opmode_streaming)
    sim.simxReadProximitySensor(clientID, irLeft, sim.simx_opmode_streaming)
    sim.simxGetVisionSensorImage(clientID, color_sensor_Left, 0, sim.simx_opmode_streaming)
    sim.simxGetVisionSensorImage(clientID, color_sensor_Right, 0, sim.simx_opmode_streaming)

    time.sleep(2)

    # # Comandos motores
    # PrintSim('comecei')
    # i = 0
    # while (i < 5):
    #     MoveForwardPosition(0.002)
    #     i += 1
    # #PrintSim('terminei')
    # #time.sleep(5)
    # MoveForwardPosition(0.0015)
    # #time.sleep(2)
    #
    # Comando Sensores

    ### TESTES ###

    MoveDirectionSquare(frente, 6)

    ##############

    cont = 0
    while (cont < 100):
        cont += 1
        # Coletar dados robôs e alvos
        [erro, [xr, yr, zr]] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_buffer)
        # [erro, [xt,yt,zt]] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_buffer)
        [erro, [alpha, beta, gamma]] = sim.simxGetObjectOrientation(clientID, robot, -1, sim.simx_opmode_buffer)

        # sim.simxAddStatusbarMessage(clientID, 'A posição em x é '+str(xr) + ' e a posição em y é '+str(yr), sim.simx_opmode_oneshot_wait)

    # Stop simulation:
    # sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot_wait)

    # Pause simulation
    sim.simxPauseSimulation(clientID, sim.simx_opmode_oneshot_wait)

    # Now close the connection to V-REP:
    sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking)
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
