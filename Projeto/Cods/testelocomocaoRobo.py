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
import graphBlocks as gb

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
frente = 1
tras = -1
direita = 1
esquerda = -1
TERCEIRO_ANDAR = 0.12
SEGUNDO_ANDAR = 0.01
PRIMEIRO_ANDAR = -0.1
cube = 0




################# TESTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE ##########################33
matrix = [
    ['R', 0, 0],
    ['W', 0, 2],
    ['G', 0, 1]   
#    ['G', 7, 2],
#    ['B', 4, 3]
]
################## TESTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE #######################

def PrintSim(mensagem):
    sim.simxAddStatusbarMessage(clientID, mensagem, sim.simx_opmode_oneshot_wait)

def TimeOut(dist, startTime):
    currenttime = time.time()
    #print(startTime, currenttime)
    if (currenttime - startTime > abs(dist*100 + 1)):
        return True
    return False

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
        erro, detectable, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(clientID, sensor, sim.simx_opmode_streaming)
    #print(erro, detectable, distancePoint, detectedObjectHandle, detectedSurface)
    distance = distancePoint[2]
    if(detectable == False):
        distance = max_distance_IR
    #print(distance)
    return distance

def getCubeHandle(sensor):
    erro = 1
    while (erro != 0): 
        erro, detectable, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(clientID, sensor, sim.simx_opmode_streaming)
    return detectedObjectHandle

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

### FUNÇÕES CUBOS
def grab(cube):
    #erro, cubo = sim.simxGetObjectHandle(clientID, cube, sim.simx_opmode_blocking)
    erro, pa = sim.simxGetObjectHandle(clientID,'Cuboid_acoplador',sim.simx_opmode_blocking)
    # erro =1
    # while erro != 0:
    #    erro = sim.simxSetObjectIntParameter(clientID, cube, sim.sim_shapeintparam_respondable, 0, sim.simx_opmode_oneshot)
    #    print('respondable', erro)
    # time.sleep(1)
    # erro = 1
    # while erro != 0:
    #    erro = sim.simxSetObjectIntParameter(clientID, cube, sim.sim_shapeintparam_static, 1, sim.simx_opmode_oneshot)
    #    print('dynamic', erro)
    # time.sleep(1)
    #print(sim.simxSetModelProperty(clientID, cubo, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot))
    #time.sleep(1)
    erro = 1
    while erro != 0:
        erro = sim.simxSetObjectParent(clientID, cube, pa, True, sim.simx_opmode_oneshot)
        #print('parent', erro)
    time.sleep(3)


def leave(cube):
    #erro, cubo = sim.simxGetObjectHandle(clientID, cube, sim.simx_opmode_blocking)
    erro, pa = sim.simxGetObjectHandle(clientID,'Cuboid_acoplador',sim.simx_opmode_blocking)
    sim.simxSetObjectParent(clientID, cube, -1, True, sim.simx_opmode_oneshot_wait)
    erro =1
    while erro != 0:
        erro = sim.simxSetObjectIntParameter(clientID, cube, sim.sim_shapeintparam_respondable, 1, sim.simx_opmode_oneshot)
        #print('respondable', erro)
    time.sleep(0.1)
    erro = 1
    while erro != 0:
       erro = sim.simxSetObjectIntParameter(clientID, cube, sim.sim_shapeintparam_static, 0, sim.simx_opmode_oneshot)
       #print('dynamic', erro)
    #print(sim.simxSetModelProperty(clientID, cubo, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot))
    time.sleep(0.1)
    
    
    
## FUNÇÕES DA GARRA ##########################################

def subir_elevador(altura):
    sim.simxSetJointTargetPosition(clientID,elevador,altura,sim.simx_opmode_oneshot) 
    time.sleep(1)

def descer_elevador():
    sim.simxSetJointTargetPosition(clientID,elevador,-0.15,sim.simx_opmode_oneshot)
    time.sleep(1)

def abrir_garra():
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetPosition(clientID,paDireita,0.04,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(clientID,paEsquerda,0.04,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    time.sleep(1)

def fechar_garra(): 
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetPosition(clientID,paDireita,0.025,sim.simx_opmode_oneshot) 
    sim.simxSetJointTargetPosition(clientID,paEsquerda,0.025,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    time.sleep(1)

def fechar_garra_total():
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetPosition(clientID,paDireita,0.01,sim.simx_opmode_oneshot) 
    sim.simxSetJointTargetPosition(clientID,paEsquerda,0.01,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    time.sleep(1)

## FUNÇÕES PEGAR CUBO ########################################

def empurrar_cubo():
    MoveDirectionPosition(tras, 0.012)
    fechar_garra_total()
    while(getDistanceIR(irLeft) > 0.01 or getDistanceIR(irRight) > 0.01):
        MoveDirectionPosition(frente, 0.001)
    MoveDirectionPosition(frente, 0.004)

def pegar_cubo():
    abrir_garra()
    descer_elevador()
    fechar_garra()
    subir_elevador(SEGUNDO_ANDAR)

def chegar_perto_prateleira():
    a = getDistanceIR(irLeft)
    b = getDistanceIR(irRight)
    while(a > 0.07 or b > 0.07):
        #print(getDistanceIR(irLeft), getDistanceIR(irRight))
        MoveDirectionPosition(frente, 0.001)
        a = getDistanceIR(irLeft)
        b = getDistanceIR(irRight)

def entregar_cubo_colorido(cube):
    descer_elevador()
    leave(cube)
    abrir_garra()
    #empurrar_cubo()
    subir_elevador(SEGUNDO_ANDAR)

def entregar_cubo_terceiro_andar(cube):
    subir_elevador(TERCEIRO_ANDAR)
    MoveDirectionPosition(frente, 0.015)
    chegar_perto_prateleira()
    abrir_garra()
    leave(cube)
    #empurrar_cubo()
    AlignBack()
    fechar_garra_total()

def entregar_cubo_segundo_andar(cube):
    subir_elevador(SEGUNDO_ANDAR)
    MoveDirectionPosition(frente, 0.015)
    chegar_perto_prateleira()
    leave(cube)
    abrir_garra()
    #empurrar_cubo()
    AlignBack()
    fechar_garra_total()

def entregar_cubo_primeiro_andar(cube):
    subir_elevador(PRIMEIRO_ANDAR)
    MoveDirectionPosition(frente, 0.015)
    chegar_perto_prateleira()
    leave(cube)
    abrir_garra()
    #empurrar_cubo()
    AlignBack()
    fechar_garra_total()

def alinhar_cubo_na_esquerda_e_pegar():
    #MoveDirectionPosition(tras, 0.015)
    descer_elevador()
    while True :
        a = getDistanceIR(irRight)
        b = getDistanceIR(irLeft)
        print(a,b)
        MoveDirectionPosition(frente, 0.001)
        if(b<0.03 or a < 0.03):
            break

    abrir_garra()
    esq=0
    while True :
        a = getDistanceIR(irRight)
        b = getDistanceIR(irLeft)
        print(a,b)
        TurnDirectionAng(direita, 1)
        # if(b<1): 
        #     esq=esq+1
        # if(a<1 and esq>0):
        #     break
        if(b<0.015):
            break
    cube = getCubeHandle(irLeft)
    TurnDirectionAng(esquerda, 5)
    time.sleep(0.5)
    # Stop()
    # TurnRight()
    # time.sleep(0.08)
    # Stop()
    print(0.06 + b)
    MoveDirectionPosition(frente, b/10.0)
    fechar_garra()
    grab(cube)
    subir_elevador(SEGUNDO_ANDAR)
    MoveDirectionPosition(tras, b/10.0)
    return cube

def alinhar_cubo_na_direita_e_pegar():
    #MoveDirectionPosition(tras, 0.015)
    descer_elevador()
    while True :
        a = getDistanceIR(irRight)
        b = getDistanceIR(irLeft)
        print(a,b)
        MoveDirectionPosition(frente, 0.001)
        if(b<0.03 or a < 0.03):
            break

    abrir_garra()
    dirt=0
    while True :
        a = getDistanceIR(irRight)
        b = getDistanceIR(irLeft)
        print(a,b)
        TurnDirectionAng(esquerda, 1)
        # if(a<1): 
        #     dirt=dirt+1
        # if(b<1 and dirt>0):
        #     break
        if(a < 0.15):
            break
    cube = getCubeHandle(irRight)
    TurnDirectionAng(direita, 5)
    time.sleep(0.5)
    # Stop()
    # TurnLeft()
    # time.sleep(0.08)
    # Stop()
    MoveDirectionPosition(frente, a/10.0)
    fechar_garra()
    grab(cube)
    print('vou subir')
    subir_elevador(SEGUNDO_ANDAR)
    print('subi')
    time.sleep(2)
    MoveDirectionPosition(tras, a/10.0)
    return cube

 

## FUNÇÕES DE LOCOMOÇAO ######################################

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
    #print(int(actualAngR * 1000), int((angref + angRight) * 1000))
    #print(int(actualAngL * 1000), int((angref + angLeft) * 1000))

    #para melhorar: em vez de usar um chute para uma volta completa, calcular o perimetro do circulo centrado no robo
    #e de raio igual a distancia entre o centro e a roda, dividir esse valor pelo perimetro da roda e
    #usar a mesma conversao que a funcao de andar reto

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
    #print(int(actualAngR * 1000), int((angref + angRight) * 1000))
    #print(int(actualAngL * 1000), int((-angref + angLeft) * 1000))


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
   # print(int(actualAngR*1000), int((angref + angRight)*1000))
        


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

    #print("To procurando a linha")
    while ((getColor(color_sensor_Left) != PRETO and getColor(color_sensor_Right) == PRETO) or (getColor(color_sensor_Left) == PRETO and getColor(color_sensor_Right) != PRETO)):
            #print("Achei a linha")
        if (getColor(color_sensor_Left) != PRETO):
            # Mover so roda esquerda
            print("Vamos girar")
            TurnDirectionAng(esquerda, 1)
            print("Girando para a esquerda")
            direita_preto = True
            #MoveDirectionPosition(frente, 0.001)
        elif (getColor(color_sensor_Right) != PRETO):
            # Mover so roda direita
            TurnDirectionAng(direita, 1)
            print("Girando para a direita")
            #MoveDirectionPosition(frente, 0.001)
            esquerda_preto = True
    #while (getColor(color_sensor_Left) != PRETO and getColor(color_sensor_Right) != PRETO)

def AlignBack():
    while (getColor(color_sensor_Left) != PRETO or getColor(color_sensor_Right) != PRETO):
        MoveDirectionPosition(tras, 0.001)

def MoveSquareForward():
    MoveDirectionPosition(frente, 0.027)
    Align()
    print('forward')

def TurnInSquare(angle): #gira no centro do quadrado e vai para ponta
    print(angle)
    Align()
    MoveDirectionPosition(tras, 0.01)
    if(angle > 0):
        TurnDirectionAng(esquerda, abs(angle))
    if(angle < 0):
        TurnDirectionAng(direita, abs(angle))
    MoveDirectionPosition(frente, 0.005)
    Align()




#### Funções de lógica de movimentação ##############################################


def realFinalPosition(finalPosition):
    stockLocals = [32, 33, 35, 36, 42, 43, 45, 46]
    deliveryLocals = [71, 72, 73, 74, 75, 76, 77]
    shelf = [14]
    if(finalPosition in deliveryLocals):
        finalPosition -= 10
    if(finalPosition in shelf):
        finalPosition += 10
    #if(finalPosition in stockLocals) #### Definir o local em que irá pegar o cubo
    return finalPosition

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

def turnTo(myDirection, finalDirection):
    if(finalDirection == NORTH):
        if(myDirection == EAST):
            TurnInSquare(90)
        if(myDirection == SOUTH):
            TurnInSquare(180)
        if(myDirection == WEST):
            TurnInSquare(-90)
        return NORTH
    if(finalDirection == EAST):
        if(myDirection == NORTH):
            TurnInSquare(-90)
        if(myDirection == SOUTH):
            TurnInSquare(90)
        if(myDirection == WEST):
            TurnInSquare(180)
        return EAST
    if(finalDirection == SOUTH):
        if(myDirection == EAST):
            TurnInSquare(-90)
        if(myDirection == NORTH):
            TurnInSquare(180)
        if(myDirection == WEST):
            TurnInSquare(90)
        return SOUTH
    if(finalDirection == WEST):
        if(myDirection == EAST):
            TurnInSquare(180)
        if(myDirection == SOUTH):
            TurnInSquare(-90)
        if(myDirection == NORTH):
            TurnInSquare(90)
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
    #Parte de cima
    if(currentPosition == 22):
        myDirection = correctDirection(myDirection, -1, axisY)
        MoveSquareForward()
        myDirection = correctDirection(myDirection, +1, axisX)
        MoveSquareForward()
        currentPosition = 31
    if(currentPosition == 23):
        myDirection = correctDirection(myDirection, +1, axisY)
        MoveSquareForward()
        myDirection = correctDirection(myDirection, +1, axisX)
        MoveSquareForward()
        currentPosition = 34
    if(currentPosition == 25):
        myDirection = correctDirection(myDirection, -1, axisY)
        MoveSquareForward()
        myDirection = correctDirection(myDirection, +1, axisX)
        MoveSquareForward()
        currentPosition = 34
    if(currentPosition == 26):
        myDirection = correctDirection(myDirection, +1, axisY)
        MoveSquareForward()
        myDirection = correctDirection(myDirection, +1, axisX)
        MoveSquareForward()
        currentPosition = 37
    #Parte de baixo
    if(currentPosition == 52):
        myDirection = turnTo(myDirection, WEST)
        MoveSquareForward()
        myDirection = turnTo(myDirection, NORTH)
        MoveSquareForward()
        currentPosition = 41
    if(currentPosition == 53):
        myDirection = turnTo(myDirection, EAST)
        MoveSquareForward()
        myDirection = turnTo(myDirection, NORTH)
        MoveSquareForward()
        currentPosition = 44
    if(currentPosition == 55):
        myDirection = turnTo(myDirection, WEST)
        MoveSquareForward()
        myDirection = turnTo(myDirection, NORTH)
        MoveSquareForward()
        currentPosition = 44
    if(currentPosition == 56):
        myDirection = turnTo(myDirection, EAST)
        MoveSquareForward()
        myDirection = turnTo(myDirection, NORTH)
        MoveSquareForward()
        currentPosition = 47

    return currentPosition, myDirection


def goFromTo(currentPosition, finalPosition, myDirection):
    finalPosition = realFinalPosition(finalPosition)
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
    return currentPosition, myDirection

def goToShelfDeliver(block, currentPosition, myDirection, cube):
    shelf1 = [1, 6, 11]
    shelf2 = [2, 7, 12]
    shelf3 = [3, 8, 13]
    shelf4 = [4, 9, 14]
    shelf5 = [5, 10, 15]
    if (block in shelf1):
        currentPosition, myDirection = goFromTo(currentPosition, 22, myDirection)
    if (block in shelf2):
        currentPosition, myDirection = goFromTo(currentPosition, 23, myDirection)
    if (block in shelf3):
        currentPosition, myDirection = goFromTo(currentPosition, 24, myDirection)
    if (block in shelf4):
        currentPosition, myDirection = goFromTo(currentPosition, 25, myDirection)
    if (block in shelf5):
        currentPosition, myDirection = goFromTo(currentPosition, 26, myDirection)

    myDirection = turnTo(myDirection, NORTH)
    if(block <= 5):
        entregar_cubo_primeiro_andar(cube)
    elif(block <= 10):
        entregar_cubo_segundo_andar(cube)
    elif(block <= 15):
        print('vou entregar')
        entregar_cubo_terceiro_andar(cube)

    return currentPosition, myDirection


def goToSquareSide(myDirection, firstDirection, finalTurn):
    #MoveDirectionPosition(tras, 0.01)
    turnTo(myDirection, firstDirection)
    Align()
    MoveDirectionPosition(tras, 0.005)
    TurnDirectionAng(finalTurn, 90)

    
        
               
### FUNÇÕES DESAFIO ###############################################################

def getBlocksInformation(currentPosition, myDirection):
    #Vai para a primeira área
    currentPosition, myDirection = goFromTo(currentPosition, 22, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = turnTo(myDirection ,EAST)
    #Align() #TurnTo ja alinha
    MoveDirectionPosition(frente, 0.005)
    TurnDirectionAng(direita, 90)
    myDirection = SOUTH
    #Usa algoritmo de visao
    ## VISAO
    time.sleep(3)
    

    #Vai para a segunda área
    myDirection = turnTo(myDirection ,EAST)
    #MoveDirectionPosition(frente, 0.020)
    currentPosition += 1
    currentPosition, myDirection = goFromTo(currentPosition, 25, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = turnTo(myDirection ,EAST)
    #Align()
    MoveDirectionPosition(frente, 0.005)
    TurnDirectionAng(direita, 90)
    myDirection = SOUTH
    #Usa algoritmo de visao
    ## VISAO
    time.sleep(3)

    myDirection = turnTo(myDirection ,EAST)
    #MoveDirectionPosition(frente, 0.020)
    currentPosition += 1
    
    order = gb.get_path(gb.createGraphBlocks(matrix))

    return currentPosition, myDirection, order, matrix

def course(block, matrix):
    delivery_locals = {'R': [74], 'Y': [73, 75], 'B': [72, 76], 'G': [71, 77], 'W': [14], 'K': [14]}
    stock_locals = {0: 32, 1: 33, 2: 42, 3:43, 4: 35, 5: 36, 6: 45, 7: 46}
    hiddenBlock = False
    blockPosition = matrix[block][2]

    #definindo quadrante para buscar bloco
    if (stock_locals[matrix[block][1]] == 32 or stock_locals[matrix[block][1]] == 35):
        if (matrix[block][2] == 0):
            blockLocalPickup = stock_locals[matrix[block][1]]
        if (matrix[block][2] == 1):
            blockLocalPickup = stock_locals[matrix[block][1]] - 10
        if (matrix[block][2] == 2):
            blockLocalPickup = stock_locals[matrix[block][1]] - 1
        if (matrix[block][2] == 3): #caso escondido
            blockLocalPickup = stock_locals[matrix[block][1]]
            hiddenBlock = True

    if (stock_locals[matrix[block][1]] == 33 or stock_locals[matrix[block][1]] == 36):
        if (matrix[block][2] == 0):
            blockLocalPickup = stock_locals[matrix[block][1]] -10
        if (matrix[block][2] == 1):
            blockLocalPickup = stock_locals[matrix[block][1]]
        if (matrix[block][2] == 2): #caso escondido
            blockLocalPickup = stock_locals[matrix[block][1]]
            hiddenBlock = True 
        if (matrix[block][2] == 3): 
            blockLocalPickup = stock_locals[matrix[block][1]] + 1
    
    if (stock_locals[matrix[block][1]] == 42 or stock_locals[matrix[block][1]] == 45):
        if (matrix[block][2] == 0):
            blockLocalPickup = stock_locals[matrix[block][1]] - 1
        if (matrix[block][2] == 1): #caso escondido
            blockLocalPickup = stock_locals[matrix[block][1]]
            hiddenBlock = True
        if (matrix[block][2] == 2):
            blockLocalPickup = stock_locals[matrix[block][1]]
        if (matrix[block][2] == 3):
            blockLocalPickup = stock_locals[matrix[block][1]] + 10
        
    if (stock_locals[matrix[block][1]] == 43 or stock_locals[matrix[block][1]] == 44):
        if (matrix[block][2] == 0): #caso escondido
            blockLocalPickup = stock_locals[matrix[block][1]]
            hiddenBlock = True
        if (matrix[block][2] == 1): 
            blockLocalPickup = stock_locals[matrix[block][1]] + 1
        if (matrix[block][2] == 2):
            blockLocalPickup = stock_locals[matrix[block][1]] + 10
        if (matrix[block][2] == 3):
            blockLocalPickup = stock_locals[matrix[block][1]]
    
    #definindo quadrante para deixar bloco
    if(matrix[block][0] == 'W' or matrix[block][0] == 'K'):
        blockLocalDelivery = delivery_locals[matrix[block][0]][0]
    elif(matrix[block][1] < 4): #Esta do lado esquerdo
        blockLocalDelivery = delivery_locals[matrix[block][0]][0]
    else: #Esta do lado direito
        blockLocalDelivery = delivery_locals[matrix[block][0]][1]

    blockColor = matrix[block][0]

    return blockLocalPickup, blockLocalDelivery, blockColor, hiddenBlock, blockPosition



def grabBlock(currentPosition, blockPosition, myDirection):
    if(currentPosition == 22 or currentPosition== 23 or currentPosition == 25 or currentPosition == 26):
        if(blockPosition == 0):
            goToSquareSide(myDirection, WEST, esquerda)
            myDirection = SOUTH
            cube = alinhar_cubo_na_direita_e_pegar()
        if(blockPosition == 1):
            goToSquareSide(myDirection, EAST, direita)
            myDirection = SOUTH
            cube = alinhar_cubo_na_esquerda_e_pegar()
    if(currentPosition == 31 or currentPosition== 41 or currentPosition == 34 or currentPosition == 44):
        if(blockPosition == 0):
            goToSquareSide(myDirection, NORTH, direita)
            myDirection = EAST
            cube = alinhar_cubo_na_esquerda_e_pegar()
        if(blockPosition == 2):
            goToSquareSide(myDirection, SOUTH, esquerda)
            myDirection = EAST
            cube = alinhar_cubo_na_direita_e_pegar()
    if(currentPosition == 52 or currentPosition== 53 or currentPosition == 55 or currentPosition == 56):
        if(blockPosition == 2):
            goToSquareSide(myDirection, EAST, direita)
            myDirection = NORTH
            cube = alinhar_cubo_na_esquerda_e_pegar()
        if(blockPosition == 3):
            goToSquareSide(myDirection, WEST, esquerda)
            myDirection = NORTH
            cube = alinhar_cubo_na_direita_e_pegar()  
    if(currentPosition == 34 or currentPosition== 44 or currentPosition == 37 or currentPosition == 47):
        if(blockPosition == 1):
            goToSquareSide(myDirection, NORTH, esquerda)
            myDirection = WEST
            cube = alinhar_cubo_na_direita_e_pegar()
        if(blockPosition == 3):
            goToSquareSide(myDirection, SOUTH, direita)
            myDirection = WEST
            cube = alinhar_cubo_na_esquerda_e_pegar()

    return myDirection, cube

    
            

def winOPEN():
    initialPosition = 11
    initialDirection = SOUTH
    #currentPosition, myDirection, order, matrix = getBlocksInformation(initialPosition, initialDirection)
    #order = [1, 2, 3]
    pickLater = []
    #APENAS TESTE
    order = gb.get_path(gb.createGraphBlocks(matrix))
    currentPosition = initialPosition
    myDirection = initialDirection
    #FIM DE TESTE
    for i in range(1, len(order)):
        blockLocalPickup, blockLocalDelivery, blockColor, hiddenBlock, blockPosition = course(order[i] - 2, matrix)
        if (not hiddenBlock):
            currentPosition, myDirection = goFromTo(currentPosition, blockLocalPickup, myDirection)
            myDirection, cube = grabBlock(currentPosition, blockPosition, myDirection)
            currentPosition, myDirection = goFromTo(currentPosition, blockLocalDelivery, myDirection)
            if(blockColor == 'K' or blockColor == 'W'):
                #identifica número
                blockNumber = 6 ##### MODIFICAR QUANDO IDENTIFICAR
                currentPosition, myDirection = goToShelfDeliver(blockNumber, currentPosition, myDirection, cube)
            else:
                entregar_cubo_colorido(cube)
        else:
            pickLater.append([blockColor, blockLocalPickup, blockLocalDelivery])






##########################################



print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID = sim.simxStart('127.0.0.1',19999,True,True,5000,5)
robotname = 'Robot'
#targetname = 'Target1'
if clientID != -1:
    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
    print ('Connected to remote API server')
    sim.simxAddStatusbarMessage(clientID,'Funcionando...',sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)

    # Coletar handles
    #Robô
    erro, robot = sim.simxGetObjectHandle(clientID, robotname, sim.simx_opmode_blocking) 
    #Motores
    [erro, robotLeftMotor] = sim.simxGetObjectHandle(clientID, 'Revolute_joint2', sim.simx_opmode_blocking)
    [erro, robotRightMotor] = sim.simxGetObjectHandle(clientID, 'Revolute_joint1', sim.simx_opmode_blocking)
    #Garra
    erro,paEsquerda=sim.simxGetObjectHandle(clientID,'joint_pa_esquerda_garra',sim.simx_opmode_blocking)
    erro,paDireita=sim.simxGetObjectHandle(clientID,'joint_pa_direita_garra',sim.simx_opmode_blocking)
    erro,elevador=sim.simxGetObjectHandle(clientID,'joint_acoplador_garra',sim.simx_opmode_blocking)
    #Sensores
    erro, irRight = sim.simxGetObjectHandle(clientID, 'Sensor_IR_direito', sim.simx_opmode_blocking)
    erro, irLeft = sim.simxGetObjectHandle(clientID, 'Sensor_IR_esquerdo', sim.simx_opmode_blocking)
    erro , color_sensor_Left = sim.simxGetObjectHandle(clientID, 'Sensor_cor_esquerda', sim.simx_opmode_blocking)
    erro , color_sensor_Right = sim.simxGetObjectHandle(clientID, 'Sensor_cor_direita', sim.simx_opmode_blocking)

    

    # Criar stream de dados
    [erro, positionrobot] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_streaming)
    #[erro, positiontarget] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_streaming)
    erro, angLeft = sim.simxGetJointPosition(clientID, robotLeftMotor, sim.simx_opmode_streaming)
    erro, angRight = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_streaming)
    [erro, orientationrobot] = sim.simxGetObjectOrientation(clientID,robot,-1,sim.simx_opmode_streaming)
    sim.simxReadProximitySensor(clientID, irRight, sim.simx_opmode_streaming)
    sim.simxReadProximitySensor(clientID, irLeft, sim.simx_opmode_streaming)
    sim.simxGetVisionSensorImage(clientID, color_sensor_Left, 0, sim.simx_opmode_streaming)
    sim.simxGetVisionSensorImage(clientID, color_sensor_Right, 0, sim.simx_opmode_streaming)

    time.sleep(2)
    initialPosition = 11
    initialDirection = SOUTH
    winOPEN()


    #getBlocksInformation(initialPosition, initialDirection)
    # TurnDirectionAng(direita, 90)
    # # time.sleep(10)
    # currentPosition, myDirection = goFromTo(initialPosition, 32, initialDirection)
    # print('cheguei pra pegar cubo')
    # currentPosition, myDirection = goFromTo(currentPosition, 14, myDirection)
    # currentPosition, myDirection = goToShelfDeliver(8, currentPosition, myDirection)
    # MoveDirectionPosition(tras, 0.01)
    # alinhar_cubo_na_direita_e_pegar()
    # currentPosition, myDirection = goFromTo(currentPosition, 71, myDirection)
    # entregar_cubo_colorido()
    erro, cube = sim.simxGetObjectHandle(clientID, 'Cuboid3', sim.simx_opmode_blocking)
    #leave(cube)
    #time.sleep(5)
   
    # erro = 1
    # while erro != 0:
    #     erro = sim.simxSetObjectIntParameter(clientID, cube, sim.sim_shapeintparam_respondable, 0, sim.simx_opmode_oneshot)
    #     print('respondable', erro)
    # erro = 1
    # time.sleep(3)
    # while erro != 0:
    #    erro = sim.simxSetObjectIntParameter(clientID, cube, sim.sim_shapeintparam_static, 1, sim.simx_opmode_oneshot)
    #    print('dynamic', erro)
    # time.sleep(3)
    # cube = alinhar_cubo_na_direita_e_pegar()
    # entregar_cubo_colorido(cube)
    
    # currentPosition, myDirection = goFromTo(currentPosition , 75, myDirection)
    #goToShelfDeliver(4, currentPosition, myDirection)
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
    #Comando Sensores
    # for i in range(2):
    #     MoveSquareForward()

    # cont = 0
    # while(cont < 100):
    #     cont+=1
    #     # Coletar dados robôs e alvos
    #     [erro, [xr,yr,zr]] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_buffer)
    #     #[erro, [xt,yt,zt]] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_buffer)
    #     [erro, [alpha, beta, gamma]] = sim.simxGetObjectOrientation(clientID, robot, -1, sim.simx_opmode_buffer)

        
        #sim.simxAddStatusbarMessage(clientID, 'A posição em x é '+str(xr) + ' e a posição em y é '+str(yr), sim.simx_opmode_oneshot_wait)

        

    # Stop simulation:
    # sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot_wait)

    # Pause simulation
    sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    # Now close the connection to V-REP:
    sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking )
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')




