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
#import graphBlocks as gb
import visionAlgo as vis
import giroAlgo as giro
import graphBlocksBetter as gbb
import firstSq

PRETO = 0
VERMELHO = 1
AMARELO = 2
VERDE = 3
AZUL = 5
BRANCO = 6
NORTH = 1
SOUTH = -1
EAST = 2
WEST = -2
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
Prateleiras = [0] * 16





################# TESTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE ##########################33
# matrix = [
#     ['R', 0, 0],
#     ['W', 0, 2],
#     ['G', 0, 1]   
# #    ['G', 7, 2],
# #    ['B', 4, 3]
# ]
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
    erro , resolution , Image = sim.simxGetVisionSensorImage(clientID, sensor, 0, sim.simx_opmode_buffer)
    while (erro != 0):
        erro , resolution , Image = sim.simxGetVisionSensorImage(clientID, sensor, 0, sim.simx_opmode_buffer)
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
    time.sleep(0.5)

def descer_elevador():
    sim.simxSetJointTargetPosition(clientID,elevador,-0.15,sim.simx_opmode_oneshot)
    time.sleep(1)

def abrir_garra():
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetPosition(clientID,paDireita,0.04,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(clientID,paEsquerda,0.04,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    time.sleep(1.5)

def fechar_garra(): 
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetPosition(clientID,paDireita,0.025,sim.simx_opmode_oneshot) 
    sim.simxSetJointTargetPosition(clientID,paEsquerda,0.025,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    time.sleep(0.5)

def fechar_garra_total():
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetPosition(clientID,paDireita, 0.015, sim.simx_opmode_oneshot) 
    sim.simxSetJointTargetPosition(clientID,paEsquerda, 0.015, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    time.sleep(0.5)

def fechar_garra_cubo(cube):
    erro = 1
    # while erro != 0:
    #     erro, robotPosition = sim.simxGetObjectPosition(clientID, robo, -1, sim.simx_opmode_streaming)
    # erro = 1
    while erro != 0:
        erro, cubePosition = sim.simxGetObjectPosition(clientID, cube, robo, sim.simx_opmode_streaming)
    #print(robotPosition)
    #print(cubePosition)
    cubePosition[0] = 0
    erro = 1
    while erro != 0:
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetPosition(clientID,paDireita,0.025,sim.simx_opmode_oneshot) 
        sim.simxSetJointTargetPosition(clientID,paEsquerda,0.025,sim.simx_opmode_oneshot)
        erro = sim.simxSetObjectPosition(clientID, cube, robo, cubePosition, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)
    time.sleep(1)

## FUNÇÕES PEGAR CUBO ########################################

def empurrar_cubo():
    MoveDirectionPosition(tras, 0.12)
    fechar_garra_total()
    while(getDistanceIR(irLeft) > 0.01 or getDistanceIR(irRight) > 0.01):
        MoveForward(2)
    Stop()
    MoveDirectionPosition(frente, 0.04)

def pegar_cubo():
    abrir_garra()
    descer_elevador()
    fechar_garra()
    subir_elevador(SEGUNDO_ANDAR)

def identificar_valor(blockColor):
    if (blockColor == 'W'):
        text, op2 = vis.getNumber(clientID)
        print(text,op2)
        if(op2[0] == -1):
            return -1
        if(op2[0] == -1):
            return 
        if(int(text) == op2[0]):
            return int(text)
        elif(op2[1] < 0.1):
            text_, op2_ = vis.getNumber(clientID)
            if(int(text_) == op2_[0]):
                return int(text_)
            elif(op2_[1] < 0.1):
                return int(op2_[0])
        return int(text)
    if(blockColor == 'K'):
        num1 = vis.getCode(clientID)
        num2 = vis.getCode(clientID)
        if(num1 == num2):
            return num1
        else:
            return identificar_valor(blockColor)
    return -2 


def chegar_perto_prateleira():
    a = getDistanceIR(irLeft)
    b = getDistanceIR(irRight)
    #print('chegando')
    MoveForward(3)
    while(a > 0.07 or b > 0.07):
        #print(getDistanceIR(irLeft), getDistanceIR(irRight))
        a = getDistanceIR(irLeft)
        b = getDistanceIR(irRight)
    Stop()

def entregar_cubo_colorido(cube):
    descer_elevador()
    leave(cube)
    abrir_garra()
    #empurrar_cubo()
    subir_elevador(SEGUNDO_ANDAR)
    fechar_garra_total()
    MoveDirectionPosition(tras, 0.05)

def entregar_cubo_terceiro_andar(cube):
    subir_elevador(TERCEIRO_ANDAR)
    MoveDirectionPosition(frente, 0.1)
    chegar_perto_prateleira()
    abrir_garra()
    leave(cube)
    #empurrar_cubo()
    AlignBack(3)
    fechar_garra_total()
    subir_elevador(SEGUNDO_ANDAR)

def entregar_cubo_segundo_andar(cube):
    #print('vou entregar')
    subir_elevador(SEGUNDO_ANDAR)
    MoveDirectionPosition(frente, 0.1)
    chegar_perto_prateleira()
    leave(cube)
    abrir_garra()
    #empurrar_cubo()
    AlignBack(3)
    fechar_garra_total()
    subir_elevador(SEGUNDO_ANDAR)

def entregar_cubo_primeiro_andar(cube):
    subir_elevador(PRIMEIRO_ANDAR)
    MoveDirectionPosition(frente, 0.1)
    chegar_perto_prateleira()
    leave(cube)
    abrir_garra()
    #empurrar_cubo()
    AlignBack(3)
    fechar_garra_total()
    subir_elevador(SEGUNDO_ANDAR)

def alinhar_cubo_na_esquerda_e_pegar():
    andar_em_metros(tras, 2, 0.01)
    fechar_garra_total()
    descer_elevador()
    while True :
        a = getDistanceIR(irRight)
        b = getDistanceIR(irLeft)
        #print(a,b)
        MoveForward(2)
        if(b<0.03 or a < 0.03):
            break
    Stop()
    a = getDistanceIR(irRight)
    b = getDistanceIR(irLeft)
    if(b < a):
        cube = getCubeHandle(irLeft)
        dist = b
    else:
        cube = getCubeHandle(irRight)
        dist = a
    abrir_garra()
    esq=0
    # while True :
    #     a = getDistanceIR(irRight)
    #     b = getDistanceIR(irLeft)
        # print(a,b)
        # giro_livre(direita, 2)
        # # if(b<1): 
        # #     esq=esq+1
    #     # if(a<1 and esq>0):
    #     #     break
    #     if(b<0.015):
    #         break
    
    #TurnDirectionAng(esquerda, 5)
    # Stop()
    # TurnRight()
    # time.sleep(0.08)
    # Stop()
    print(dist)
    andar_em_metros(frente, 2, dist)
    fechar_garra_cubo(cube)
    grab(cube)
    subir_elevador(SEGUNDO_ANDAR)
    AlignSpecial(2)
    #MoveDirectionPosition(tras, dist)
    return cube

def alinhar_cubo_na_direita_e_pegar():
    andar_em_metros(tras, 2, 0.01)
    fechar_garra_total()
    descer_elevador()
    while True :
        a = getDistanceIR(irRight)
        b = getDistanceIR(irLeft)
        #print(a,b)
        
        if(b<0.03 or a < 0.03):
            break
        MoveForward(2)
    Stop()
    a = getDistanceIR(irRight)
    b = getDistanceIR(irLeft)
    if(b < a):
        cube = getCubeHandle(irLeft)
        dist = b
    else:
        cube = getCubeHandle(irRight)
        dist = a
    abrir_garra()

    dirt=0
    # while True :
    #     a = getDistanceIR(irRight)
    #     b = getDistanceIR(irLeft)
    #     print(a,b)
    #     giro_livre(esquerda, 2)
    #     # if(a<1): 
    #     #     dirt=dirt+1
    #     # if(b<1 and dirt>0):
    #     #     break
    #     if(a < 0.15):
    #         break
    Stop()

    #TurnDirectionAng(direita, 5)
    # Stop()
    # TurnLeft()
    # time.sleep(0.08)
    # Stop()
    andar_em_metros(frente, 2, dist)

    fechar_garra_cubo(cube)
    grab(cube)
    print('vou subir')
    subir_elevador(SEGUNDO_ANDAR)
    print('subi')
    AlignSpecial(2)
    #time.sleep(2)
    #MoveDirectionPosition(tras, dist)
    return cube

 

## FUNÇÕES DE LOCOMOÇAO ######################################

def Stop():
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,robotRightMotor, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,robotLeftMotor, 0, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def MoveForward(v):
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,robotRightMotor, v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,robotLeftMotor, v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def MoveBack(v):
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,robotRightMotor, -v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,robotLeftMotor, -v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def MoveDirectionPosition(direcao, dist):   #Andar reto para frente ou para trás
    andar_em_metros(direcao, 5, dist)

def TurnDirectionAng(direcao, ang):   #Girar para a direita ou para a esquerda pelo angulo que você escolher
    if (ang == 180):
        giro.Girar_180_graus_v2(clientID, robotRightMotor, robotLeftMotor, robo)
    else:
        giro.Girar_90_graus_v2(clientID, robotRightMotor, robotLeftMotor, robo, direcao)


def andar_em_metros(d,v,m):
    
    # d = 1 , andar para frente
    # d =-1 , andar para trás
    # v = velocidade
    # m = valor em metros

    erro,a_inicial=sim.simxGetObjectPosition(clientID,robo,-1,sim.simx_opmode_blocking)
    x_inicial=a_inicial[0]
    y_inicial=a_inicial[1]
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor,d*v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor,d*v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    while(True):
        erro,a=sim.simxGetObjectPosition(clientID,robo,-1,sim.simx_opmode_blocking)
        x=a[0]
        y=a[1]
        #print(x,y)
        if(abs(x-x_inicial)>=m or abs(y-y_inicial)>=m): 
            break 
    Stop()

def giro_livre(d,v):
    
    # d = 1 , anti horario, esquerda
    # d =-1 , horario, direita
    # v = velocidade

    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def girar_90_graus(d,v):

    # d = 1 , anti horario, esquerda
    # d =-1 , horario, direita
    # v = velocidade
    
    g = 90
    erro,b_inicial=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
    gamma_inicial=b_inicial[2]
    gamma_inicial=gamma_inicial*57.2958

    if((gamma_inicial<=-170 and gamma_inicial>=-190) or gamma_inicial>170 and gamma_inicial<190):        
        while(True):
            erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
            gamma=b[2]
            gamma=gamma*57.2958
            #print(gamma)
            if(abs(abs(gamma)-abs(gamma_inicial))>=g):
                while(True):
                    erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
                    gamma=b[2]
                    gamma=gamma*57.2958
                    if(abs(abs(gamma)-abs(gamma_inicial))<=g):
                        break
                    sim.simxPauseCommunication(clientID, True)
                    sim.simxSetJointTargetVelocity(clientID,robotRightMotor,(-1)*d*0.2, sim.simx_opmode_oneshot)
                    sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,d*0.2, sim.simx_opmode_oneshot)
                    sim.simxPauseCommunication(clientID, False)
                    #print(gamma_inicial,gamma)
                break
            sim.simxPauseCommunication(clientID, True)
            sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
            sim.simxPauseCommunication(clientID, False)
            #print(gamma_inicial,gamma)

    else:
        while(True):
            erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
            gamma=b[2]
            gamma=gamma*57.2958
            #print(gamma)
            if(abs(gamma-gamma_inicial)>=g):
                while(True):
                    erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
                    gamma=b[2]
                    gamma=gamma*57.2958
                    if(abs(gamma-gamma_inicial)<=g):
                        break
                    sim.simxPauseCommunication(clientID, True)
                    sim.simxSetJointTargetVelocity(clientID,robotRightMotor,(-1)*d*0.2, sim.simx_opmode_oneshot)
                    sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,d*0.2, sim.simx_opmode_oneshot)
                    sim.simxPauseCommunication(clientID, False)
                    #print(gamma_inicial,gamma)
                break
            sim.simxPauseCommunication(clientID, True)
            sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
            sim.simxPauseCommunication(clientID, False)
            #print(gamma_inicial,gamma)



def Girar_180_graus(): 
    
    # d = 1 , anti horario, esquerda
    # d =-1 , horario, direita
    # v = velocidade
    v = 5
    d = -1
    g = 90

    #gira 90:

    erro,b_inicial=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
    gamma_inicial=b_inicial[2]
    gamma_inicial=gamma_inicial*57.2958
    if((gamma_inicial<=-170 and gamma_inicial>=-190) or gamma_inicial>170 and gamma_inicial<190):                
        while(True):
            erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
            gamma=b[2]
            gamma=gamma*57.2958           
            if(abs(abs(gamma)-abs(gamma_inicial))>=0.9*g):
                break
            sim.simxPauseCommunication(clientID, True)
            sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
            sim.simxPauseCommunication(clientID, False)
    else:
        while(True):
            erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
            gamma=b[2]
            gamma=gamma*57.2958   
            if(abs(gamma-gamma_inicial)>=0.9*g):
                break
            sim.simxPauseCommunication(clientID, True)
            sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
            sim.simxPauseCommunication(clientID, False)

    #gira 90 dnv:

    erro,b_inicial=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
    gamma_inicial=b_inicial[2]
    gamma_inicial=gamma_inicial*57.2958
    if((gamma_inicial<=-170 and gamma_inicial>=-190) or gamma_inicial>170 and gamma_inicial<190):        
        while(True):
            erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
            gamma=b[2]
            gamma=gamma*57.2958
            if(abs(abs(gamma)-abs(gamma_inicial))>=0.9*g):
                break
            sim.simxPauseCommunication(clientID, True)
            sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
            sim.simxPauseCommunication(clientID, False) 
        Stop()
        erro,b_inicial=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
        gamma_inicial=b_inicial[2]
        gamma_inicial=gamma_inicial*57.2958
        while(True):
            erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
            gamma=b[2]
            gamma=gamma*57.2958
            if(abs(abs(gamma)-abs(gamma_inicial))>=0.05*g):
                break
            sim.simxPauseCommunication(clientID, True)
            sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*0.4, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*0.4, sim.simx_opmode_oneshot)
            sim.simxPauseCommunication(clientID, False)
    else:
        while(True):
            erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
            gamma=b[2]
            gamma=gamma*57.2958
            if(abs(gamma-gamma_inicial)>=0.9*g):
                break
            sim.simxPauseCommunication(clientID, True)
            sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
            sim.simxPauseCommunication(clientID, False)
        Stop()
        erro,b_inicial=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
        gamma_inicial=b_inicial[2]
        gamma_inicial=gamma_inicial*57.2958
        while(True):
            erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
            gamma=b[2]
            gamma=gamma*57.2958
            if(abs(gamma-gamma_inicial)>=0.05*g):
                break
            sim.simxPauseCommunication(clientID, True)
            sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*0.4, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*0.4, sim.simx_opmode_oneshot)
            sim.simxPauseCommunication(clientID, False) 
    Stop()

def MoveForwardPosition(dist):
    MoveDirectionPosition(frente, dist)



def gira_livre_uma_roda(roda, d, v):
         
            # roda: escolher com qual roda girar
            # d = 1 , anti horario
            # d = -1 , horario
            # v = velocidade  
    if (roda == direita):        
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, d*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(clientID,robotRightMotor, 0, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)       
    elif(roda == esquerda):      
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, 0, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(clientID, robotRightMotor, -d*v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

      

def Align():   #em desenvolvimento
    v = 2
    direita_preto = False
    esquerda_preto = False
    sim.simxGetObjectPosition(clientID, color_sensor_Left, -1, sim.simx_opmode_streaming)
    sim.simxGetObjectPosition(clientID, color_sensor_Right, -1, sim.simx_opmode_streaming)

    while(True):

        if (getColor(color_sensor_Left) == PRETO or getColor(color_sensor_Right) == PRETO):
            #print("To procurando a linha")
            #print("Achei pela primeira vez")
            break

        MoveForward(v)

    Stop()
    [erro, pri_pos_cor_dir] = sim.simxGetObjectPosition(clientID, color_sensor_Right, -1, sim.simx_opmode_buffer)
    #print(erro, pri_pos_cor_dir)
    [erro, pri_pos_cor_esq] = sim.simxGetObjectPosition(clientID, color_sensor_Left, -1, sim.simx_opmode_buffer)
    #print(erro, pri_pos_cor_esq)

    if (getColor(color_sensor_Left) == PRETO):
        esquerda_preto = True

        while(True):

            if (getColor(color_sensor_Right) == PRETO):
                #print("Achei pela segunda vez direito")
                break

            MoveForward(v)

    elif (getColor(color_sensor_Right) == PRETO):
        direita_preto = True

        while(True):

            if (getColor(color_sensor_Left) == PRETO):
                #print("Achei pela segunda vez esquerdo")
                break

            MoveForward(v)

    Stop()
    [erro, seg_pos_cor_dir] = sim.simxGetObjectPosition(clientID, color_sensor_Right, -1, sim.simx_opmode_buffer)
    #print(erro, seg_pos_cor_dir)
    [erro, seg_pos_cor_esq] = sim.simxGetObjectPosition(clientID, color_sensor_Left, -1, sim.simx_opmode_buffer)
    #print(erro, seg_pos_cor_esq)
    #A essa altura, o robô já andou, viu a linha com o primeiro sensor, andou mais e viu a linha com o segundo

    linha_vertical = False
    linha_horizontal = False

    x_p_dif_trans = np.abs(pri_pos_cor_dir[0] - pri_pos_cor_esq[0])
    x_s_dif_trans = np.abs(seg_pos_cor_dir[0] - seg_pos_cor_esq[0])
    x_e_dif_longi = np.abs(pri_pos_cor_esq[0] - seg_pos_cor_esq[0])
    x_d_dif_longi = np.abs(pri_pos_cor_dir[0] - seg_pos_cor_dir[0])

    y_p_dif_trans = np.abs(pri_pos_cor_dir[1] - pri_pos_cor_esq[1])
    y_s_dif_trans = np.abs(seg_pos_cor_dir[1] - seg_pos_cor_esq[1])
    y_e_dif_longi = np.abs(pri_pos_cor_esq[1] - seg_pos_cor_esq[1])
    y_d_dif_longi = np.abs(pri_pos_cor_dir[1] - seg_pos_cor_dir[1])


        ######################################################################
        ##### TABELA EXPLICATIVA #####
        #Essa tabela vale para x e para y, mas separadamente
        #S*n = "sensor" + lado (d=direita, e=esquerda) + vez que viu a linha (1a ou 2a)
        #dif = diferenca
        #trans = transversal (sempre compara direita e esquerda)
        #longi = longitudinal (sempre compara o mesmo lado)
        #cruz = cruzada (existe e eh diferente de zero, mas nao sera utilizada)
        #p = primeira (1a = 1), s = segunda (2a = 2)
        #
        #    |      SE1      |      SD1      |      SE2      |      SD2      |
        #SE1 |       0       |  p_dif_trans  |  e_dif_longi  | -ed_dif_cruz- |
        #SD1 |  p_dif_trans  |       0       | -de_dif_cruz- |  d_dif_longi  |
        #SE2 |  e_dif_longi  | -de_dif_cruz- |       0       |  s_dif_trans  |
        #SD2 | -ed_dif_cruz- |  d_dif_longi  |  s_dif_trans  |       0       |



    if(x_s_dif_trans > y_s_dif_trans):
        #print('desalinhado horizontal')
        linha_horizontal = True

        if (esquerda_preto == True):

            if(y_e_dif_longi > 1):
                print("Estou descentralizado para a esquerda")
                #criar funcao que recentraliza
            else:
                while(True):

                    [erro, atual_pos_cor_esq] = sim.simxGetObjectPosition(clientID, color_sensor_Left, -1, sim.simx_opmode_buffer)
                    ye_atual_dif_longi = np.abs(seg_pos_cor_esq[1] - atual_pos_cor_esq[1])

                    if(int(ye_atual_dif_longi*1000000) >= int(y_s_dif_trans*1000000)):
                        # print("Alinhando")
                        # print("Alinhei")
                        # print(int(ye_atual_dif_longi*100000))
                        # print(int(y_s_dif_trans*100000))
                        break

                    gira_livre_uma_roda(esquerda, 1, 0.3)



        elif (direita_preto == True):

            if(y_d_dif_longi > 1):
                print("Estou descentralizado para a direita")
                #criar funcao que recentraliza
            else:
                while(True):

                    [erro, atual_pos_cor_dir] = sim.simxGetObjectPosition(clientID, color_sensor_Right, -1, sim.simx_opmode_buffer)
                    yd_atual_dif_longi = np.abs(seg_pos_cor_dir[1] - atual_pos_cor_dir[1])

                    if(int(yd_atual_dif_longi*1000000) >= int(y_s_dif_trans*1000000)):
                        # print("Alinhando")
                        # print("Alinhei")
                        # print(int(yd_atual_dif_longi*1000000))
                        # print(int(y_s_dif_trans*1000000))
                        break

                    gira_livre_uma_roda(direita, -1, 0.3)


    elif(x_s_dif_trans < y_s_dif_trans):
        # print('desalinhado vertical')
        linha_vertical = True

        if (esquerda_preto == True):

            if (x_e_dif_longi > 1):
                print("Estou descentralizado para a esquerda")
                # criar funcao que recentraliza
            else:
                while (True):

                    [erro, atual_pos_cor_esq] = sim.simxGetObjectPosition(clientID, color_sensor_Left, -1, sim.simx_opmode_buffer)
                    xe_atual_dif_longi = np.abs(seg_pos_cor_esq[0] - atual_pos_cor_esq[0])

                    if (int(xe_atual_dif_longi*1000000) >= int(x_s_dif_trans*1000000)):
                        # print("Alinhando")
                        # print("Alinhei")
                        # print(int(xe_atual_dif_longi*1000000))
                        # print(int(x_s_dif_trans*1000000))
                        break

                    gira_livre_uma_roda(esquerda, 1, 0.3)

        elif (direita_preto == True):

            if (x_d_dif_longi > 1):
                print("Estou descentralizado para a direita")
                # criar funcao que recentraliza
            else:
                while (True):

                    [erro, atual_pos_cor_dir] = sim.simxGetObjectPosition(clientID, color_sensor_Right, -1, sim.simx_opmode_buffer)
                    xd_atual_dif_longi = np.abs(seg_pos_cor_dir[0] - atual_pos_cor_dir[0])

                    if (int(xd_atual_dif_longi*1000000) >= int(x_s_dif_trans*1000000)):
                        # print("Alinhando")
                        # print("Alinhei")
                        # print(xd_atual_dif_longi)
                        # print(x_s_dif_trans)
                        break

                    gira_livre_uma_roda(direita, -1, 0.3)




    Stop()
    # print("Parei de girar")

    # if (getColor(color_sensor_Left) != PRETO):
    #     print("Esquerdo branco")
    # else:  # (getColor(color_sensor_Right) == PRETO):
    #     print("Esquerdo preto")
    # if (getColor(color_sensor_Right) != PRETO):
    #     print("Direito branco")
    # else:  # (getColor(color_sensor_Left) == PRETO):
    #     print("Direito preto")


def AlignBack(v):
    while (getColor(color_sensor_Left) != PRETO or getColor(color_sensor_Right) != PRETO):
        MoveBack(v)

def AlignSpecial(v):
    leftLine = True
    rightLine = True
    while (leftLine or rightLine):
        if(getColor(color_sensor_Left) == PRETO):
            leftLine = False
        if(getColor(color_sensor_Right) == PRETO):
            rightLine = False
        MoveForward(v)
    Stop()

def MoveSquareForward():
    andar_em_metros(frente, 6, 0.23)
    Align()


def TurnInSquare(angle): #gira no centro do quadrado e vai para ponta
    print(angle)
    
    Align()
    MoveDirectionPosition(tras, 0.065)
    if(angle > 0):
        TurnDirectionAng(esquerda, abs(angle))
    if(angle < 0):
        TurnDirectionAng(direita, abs(angle))
    #MoveDirectionPosition(frente, 0.025)
    Align()


###### Funções Posição Inicial #####################################################

def inicio_virar_SUL(): # para a função COM VISÃO
    
    d=0

    while(True):
        
        erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
        gamma=(b[2]*180)/(np.pi)

        if(gamma>=-3 and gamma<=3):
            Stop()
            break

        if(d==0):
            if(gamma>0 and gamma<179.99):
                d = -1
            else:
                d = 1

        v=4
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

    Align()
    return

def inicio_virar_NORTE(): # para a função SEM VISÃO; lembrar de adicionar no if(nao viu prataleira) virar 180.

    d=0

    while(True):
        
        erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
        gamma=(b[2]*180)/(np.pi)

        if(gamma>=177 or gamma<=-177):
            Stop()
            break

        if(d==0):
            if(gamma>0 and gamma<179.99):
                d = 1
            else:
                d =-1
        
        v=4
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

    Align()
    return

def inicio_virar_SUL(): # para a função COM VISÃO
    
    d=0

    while(True):
        
        erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
        gamma=(b[2]*180)/(np.pi)

        if(gamma>=-3 and gamma<=3):
            Stop()
            break

        if(d==0):
            if(gamma>0 and gamma<179.99):
                d = -1
            else:
                d = 1

        v=4
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

    Align()
    return

def find_initial_position(): ###SEM VISÃO

    d=getDistanceIR(irRight)
    
    # se ele foi colocado virado pra prateleira => são os casos em q a posição inicial é: 12,22,13,23,15,25,16,26
    inicio_virar_NORTE()
    if(d!=1): 
        if(d<0.237141400576):
            l=1
        else:
            l=2
        TurnInSquare(90)
        while(True):
            if(not getDistanceUS(usLateral)):
                break
            MoveSquareForward()
        Stop()
        c=1
        return 10*l+c

    # se o robo é colocado virado pras cores => são todos os demais casos de posição inicial.

    else:    
        TurnDirectionAng(esquerda, 180) 
        while(True):
            a=getColor(color_sensor_Right)
            b=getColor(color_sensor_Left)
            if((a!=BRANCO and a!=PRETO) or (b!=BRANCO and b!=PRETO)):
                break
            MoveSquareForward()
            andar_em_metros(tras,2,0.05) #testar valor
        #l=7
        if(a==VERMELHO or b==VERMELHO):
            return 74      
        
        TurnInSquare(-90)

        Align()
        andar_em_metros(frente,2,0.03) #testar valor

        if(a==VERDE or b==VERDE):
            
            if(a==BRANCO or b==BRANCO):
                andar_em_metros(tras,2,0.03)#testar valor
                return 71
            elif(a==AZUL or b==AZUL):
                andar_em_metros(tras,2,0.03)#testar valor
                return 77

        elif(a==AZUL or b==AZUL):
            
            if(a==VERDE or b==VERDE):
                andar_em_metros(tras,2,0.03)#testar valor
                return 72
            elif(a==AMARELO or b==AMARELO):
                andar_em_metros(tras,2,0.03)#testar valor
                return 76

        elif(a==AMARELO or b==AMARELO):
            
            if(a==AZUL or b==AZUL):
                andar_em_metros(tras,2,0.03)#testar valor
                return 73
            elif(a==VERMELHO or b==VERMELHO):
                andar_em_metros(tras,2,0.03)#testar valor
                return 75


            

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
        #time.sleep(1)
    return currentPosition, myDirection

def shelfPosition(block, myDirection):
    if(Prateleiras[block] != 0):
        goToSquareSide(myDirection, EAST, esquerda)
        AlignSpecial(2)
        return NORTH
    
    return myDirection

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

    myDirection = shelfPosition(block, myDirection)
    
    myDirection = turnTo(myDirection, NORTH)
    
    if(block <= 5):
        entregar_cubo_primeiro_andar(cube)
    elif(block <= 10):
        entregar_cubo_segundo_andar(cube)
    elif(block <= 15):
        entregar_cubo_terceiro_andar(cube)
    Prateleiras[block] += 1

    return currentPosition, myDirection


def goToSquareSide(myDirection, firstDirection, finalTurn):
    #MoveDirectionPosition(tras, 0.01)
    if(myDirection == -firstDirection):
    #if(False):
        andar_em_metros(tras, 5, 0.10)
        AlignBack(2)
        andar_em_metros(frente, 2, 0.13)
        TurnDirectionAng(-finalTurn, 90)
    else:
        print('virando', firstDirection)
        turnTo(myDirection, firstDirection)
        Align()
        MoveDirectionPosition(tras, 0.005)
        print('virando', finalTurn)
        TurnDirectionAng(finalTurn, 90)
    #MoveDirectionPosition(tras, 0.01)

    
        
               
### FUNÇÕES DESAFIO ###############################################################

def firstCorrection(i, myDirection, currentPosition, blockLocalPickup):
    print(i, myDirection, currentPosition, blockLocalPickup)
    if(i == 0):
        if(currentPosition < 30):
            if(currentPosition % 10 > 4):
                if(blockLocalPickup % 10 >= 6):
                    print('east')
                    myDirection = turnTo(myDirection, EAST)
                    currentPosition  = 26
                else:
                    print('west')
                    myDirection = turnTo(myDirection, WEST)
                    currentPosition = 25
            else:
                if(blockLocalPickup % 10 >= 2):
                    print('east')
                    myDirection = turnTo(myDirection, EAST)
                    currentPosition = 23
                else:
                    print('west')
                    myDirection = turnTo(myDirection, WEST)
                    currentPosition = 22
        else:
            if(currentPosition % 10 > 4):
                if(blockLocalPickup % 10 >= 6):
                    print('east')
                    myDirection = turnTo(myDirection, EAST)
                    currentPosition  = 56
                else:
                    print('west')
                    myDirection = turnTo(myDirection, WEST)
                    currentPosition = 55
            else:
                if(blockLocalPickup % 10 >= 2):
                    print('east')
                    myDirection = turnTo(myDirection, EAST)
                    currentPosition = 53
                else:
                    print('west')
                    myDirection = turnTo(myDirection, WEST)
                    currentPosition = 52
        #andar_em_metros(frente, 5, 0.15)
        Align()
        print(currentPosition)
    return myDirection, currentPosition

def solvePath(matrix, currentPosition):
    matrixW, matrixK, matrixRGB, matrixFinal = gbb.separateMatrix(matrix)
    firstOrder = []
    secondOrder = []
    thirdOrder = []
    if(len(matrixW) != 0):
        #print('W', np.array(matrixW).ndim)
        if(np.array(matrixW).ndim == 1):
            firstOrder = [1, 2]
        else:    
            firstOrder = gbb.get_path(gbb.createGraphBlocks(matrixW, currentPosition))
        print('first', firstOrder)
    if(len(matrixK) != 0):
       #print('K', matrixK.ndim)
        if(np.array(matrixK).ndim == 1):
            secondOrder = [1, 2]
        else: 
            secondOrder = gbb.get_path(gbb.createGraphBlocks(matrixK, currentPosition)) #melhorar a condicao inicial
        print('second', secondOrder)
    if(len(matrixRGB) != 0):
        #print('RGB', matrixRGB.ndim)
        if(np.array(matrixRGB).ndim == 1):
            thirdOrder = [1, 2]
        else: 
            thirdOrder = gbb.get_path(gbb.createGraphBlocks(matrixRGB, currentPosition))
        print( 'third', thirdOrder)
    finalOrder = gbb.groupPaths(firstOrder, secondOrder, thirdOrder)
    return finalOrder, matrixFinal

def firstAreaCubes(currentPosition, myDirection, order):
    if(order == 1):
        destine = 22
        direction = EAST
        lastTurn = direita
    if(order == 2):
        destine = 23
        direction = WEST
        lastTurn = esquerda
    #Vai para a primeira área
    currentPosition, myDirection = goFromTo(currentPosition, destine, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = turnTo(myDirection ,direction)
    #Align() #TurnTo ja alinha
    MoveDirectionPosition(frente, 0.05)
    TurnDirectionAng(lastTurn, 90)
    myDirection = SOUTH
    matrix0 = vis.resolveVision(clientID,0)
    #time.sleep(3)
    return matrix0, currentPosition, myDirection

def secondAreaCubes(currentPosition, myDirection, order):
    #Vai para a segunda área
    # myDirection = turnTo(myDirection ,EAST)
    # #MoveDirectionPosition(frente, 0.020)
    # currentPosition += 1
    if(order == 2):
        destine = 25
        direction = EAST
        lastTurn = direita
    if(order == 1):
        destine = 26
        direction = WEST
        lastTurn = esquerda
    currentPosition, myDirection = goFromTo(currentPosition, destine, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = turnTo(myDirection ,direction)
    #Align()
    MoveDirectionPosition(frente, 0.05)
    TurnDirectionAng(lastTurn, 90)
    myDirection = SOUTH
    matrix1 = vis.resolveVision(clientID,1)
    return matrix1, currentPosition, myDirection

def thirdAreaCubes(currentPosition, myDirection, order):
    if(order == 1):
        destine = 52
        direction = EAST
        lastTurn = esquerda
    if(order == 2):
        destine = 53
        direction = WEST
        lastTurn = direita
    #Vai para a primeira área
    currentPosition, myDirection = goFromTo(currentPosition, destine, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = turnTo(myDirection ,direction)
    #Align() #TurnTo ja alinha
    MoveDirectionPosition(frente, 0.05)
    TurnDirectionAng(lastTurn, 90)
    myDirection = NORTH
    matrix0 = vis.resolveVision(clientID,0) ####ALTERAR A MATRIZ
    matrix0 = gbb.invertMatrix(matrix0)
    #time.sleep(3)
    return matrix0, currentPosition, myDirection

def fourthAreaCubes(currentPosition, myDirection, order):
    #Vai para a segunda área
    # myDirection = turnTo(myDirection ,EAST)
    # #MoveDirectionPosition(frente, 0.020)
    # currentPosition += 1
    if(order == 2):
        destine = 55
        direction = EAST
        lastTurn = esquerda
    if(order == 1):
        destine = 56
        direction = WEST
        lastTurn = direita
    currentPosition, myDirection = goFromTo(currentPosition, destine, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = turnTo(myDirection ,direction)
    #Align()
    MoveDirectionPosition(frente, 0.05)
    TurnDirectionAng(lastTurn, 90)
    myDirection = NORTH
    matrix1 = vis.resolveVision(clientID,1) #MODIFICAR MATRIZ
    matrix1 = gbb.invertMatrix(matrix1)
    return matrix1, currentPosition, myDirection


def getBlocksInformation(currentPosition, myDirection):
    print(currentPosition)
    if (currentPosition < 40): #Ta na parte de cima
        if(currentPosition % 10 <= 4):
            matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 1)
            #Vai para a segunda área
            myDirection = turnTo(myDirection ,EAST)
            #MoveDirectionPosition(frente, 0.020)
            currentPosition += 1
            matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 2)
        else:
            matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 1)
            myDirection = turnTo(myDirection ,WEST)
            currentPosition -= 1
            matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 2)
    else: #Ta na parte de baixo
        if(currentPosition % 10 <= 4):
            matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 1)
            #Vai para a segunda área
            myDirection = turnTo(myDirection ,EAST)
            #MoveDirectionPosition(frente, 0.020)
            currentPosition += 1
            matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 2)
        else:
            matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 1)
            myDirection = turnTo(myDirection ,WEST)
            currentPosition -= 1
            matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 2)

    #time.sleep(3)

    #myDirection = turnTo(myDirection ,WEST)
    #MoveDirectionPosition(frente, 0.020)
    #currentPosition += 1
    # print(matrix0)
    # print(matrix1)
    matrix = np.concatenate((matrix0, matrix1), axis=0)
    
    #order = gb.get_path(gb.createGraphBlocks(matrix))  #AQUI FUNCIONA COM O CODIGO SIMPLES!!!!!
    order, matrixFinal = solvePath(matrix, currentPosition)
    order, matrixFinal = solvePath(matrix, currentPosition)
    print(order, matrixFinal)
    

    return currentPosition, myDirection, order, matrixFinal

def course(block, matrix):
    delivery_locals = {'R': [74], 'Y': [73, 75], 'B': [72, 76], 'G': [71, 77], 'W': [14], 'K': [14]}
    stock_locals = {0: 32, 1: 33, 2: 42, 3:43, 4: 35, 5: 36, 6: 45, 7: 46}
    hiddenBlock = False
    blockPosition = int(matrix[block][2])
    stockLocal = stock_locals[int(matrix[block][1])]
    squarePosition = int(matrix[block][2])
    blockSquare = int(matrix[block][1])

    #definindo quadrante para buscar bloco
    if (stockLocal == 32 or stockLocal == 35):
        if (squarePosition == 0):
            blockLocalPickup = stockLocal
        if (squarePosition == 1):
            blockLocalPickup = stockLocal - 10
        if (squarePosition == 2):
            blockLocalPickup = stockLocal - 1
        if (squarePosition == 3): #caso escondido
            blockLocalPickup = stockLocal
            hiddenBlock = True

    if (stockLocal == 33 or stockLocal == 36):
        if (squarePosition == 0):
            blockLocalPickup = stockLocal -10
        if (squarePosition == 1):
            blockLocalPickup = stockLocal
        if (squarePosition == 2): #caso escondido
            blockLocalPickup = stockLocal
            hiddenBlock = True 
        if (squarePosition == 3): 
            blockLocalPickup = stockLocal + 1
    
    if (stockLocal == 42 or stockLocal == 45):
        if (squarePosition == 0):
            blockLocalPickup = stockLocal - 1
        if (squarePosition == 1): #caso escondido
            blockLocalPickup = stockLocal
            hiddenBlock = True
        if (squarePosition == 2):
            blockLocalPickup = stockLocal
        if (squarePosition == 3):
            blockLocalPickup = stockLocal + 10
        
    if (stockLocal == 43 or stockLocal == 46):
        if (squarePosition == 0): #caso escondido
            blockLocalPickup = stockLocal
            hiddenBlock = True
        if (squarePosition == 1): 
            blockLocalPickup = stockLocal + 1
        if (squarePosition == 2):
            blockLocalPickup = stockLocal + 10
        if (squarePosition == 3):
            blockLocalPickup = stockLocal
    
    #definindo quadrante para deixar bloco
    if(matrix[block][0] == 'W' or matrix[block][0] == 'K' or matrix[block][0] == 'R'):
        blockLocalDelivery = delivery_locals[matrix[block][0]][0]
    elif(int(matrix[block][1]) < 4): #Esta do lado esquerdo
        blockLocalDelivery = delivery_locals[matrix[block][0]][0]
    else: #Esta do lado direito
        blockLocalDelivery = delivery_locals[matrix[block][0]][1]

    blockColor = matrix[block][0]

    return blockLocalPickup, blockLocalDelivery, blockColor, hiddenBlock, blockPosition, blockSquare

def courseLastBlocks(blockSquare, blockPosition, blockZero, blockLocalPickup):
    if(len(blockZero) != 0):
        if(blockSquare == 0 or blockSquare == 4):
            if((blockZero[0][0] == 0 or blockZero[0][0] == 4) and blockZero[0][1] == 1):
                blockLocalPickup -= 1
            if((blockZero[0][0] == 0 or blockZero[0][0] == 4) and blockZero[0][1] == 2):
                blockLocalPickup -= 10
        if(blockSquare == 1 or blockSquare == 5):
            if((blockZero[0][0] == 1 or blockZero[0][0] == 5) and blockZero[0][1] == 0):
                blockLocalPickup += 1
            if((blockZero[0][0] == 1 or blockZero[0][0] == 5) and blockZero[0][1] == 3):
                blockLocalPickup -= 10
        if(blockSquare == 2 or blockSquare == 6):
            if((blockZero[0][0] == 2 or blockZero[0][0] == 6) and blockZero[0][1] == 0):
                blockLocalPickup += 10
            if((blockZero[0][0] == 2 or blockZero[0][0] == 6) and blockZero[0][1] == 3):
                blockLocalPickup -= 1
        if(blockSquare == 3 or blockSquare == 7):
            if((blockZero[0][0] == 3 or blockZero[0][0] == 7) and blockZero[0][1] == 1):
                blockLocalPickup += 10
            if((blockZero[0][0] == 3 or blockZero[0][0] == 7) and blockZero[0][1] == 2):
                blockLocalPickup += 1

    return blockLocalPickup


def grabBlock(currentPosition, blockPosition, myDirection, blockColor, blockSquare):
    print('grabBLock', currentPosition, blockPosition, myDirection, blockSquare)
    cube = robo
    if(currentPosition == 22 or currentPosition== 23 or currentPosition == 25 or currentPosition == 26):
        if(blockPosition == 0 or blockPosition == 3):
            goToSquareSide(myDirection, WEST, esquerda)
            myDirection = SOUTH
            blockNumber = identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = alinhar_cubo_na_direita_e_pegar()
        if(blockPosition == 1 or blockPosition == 2):
            goToSquareSide(myDirection, EAST, direita)
            myDirection = SOUTH
            blockNumber = identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = alinhar_cubo_na_esquerda_e_pegar()
    if(currentPosition == 31 or currentPosition== 41 or ((currentPosition == 34 or currentPosition == 44) and (blockSquare > 3))):
        if(blockPosition == 0 or blockPosition == 1):
            goToSquareSide(myDirection, NORTH, direita)
            myDirection = EAST
            blockNumber = identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = alinhar_cubo_na_esquerda_e_pegar()
        if(blockPosition == 2  or blockPosition == 3):
            goToSquareSide(myDirection, SOUTH, esquerda)
            myDirection = EAST
            blockNumber = identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = alinhar_cubo_na_direita_e_pegar()
    if(currentPosition == 52 or currentPosition== 53 or currentPosition == 55 or currentPosition == 56):
        if(blockPosition == 2  or blockPosition == 0):
            goToSquareSide(myDirection, WEST, direita)
            myDirection = NORTH
            blockNumber = identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = alinhar_cubo_na_esquerda_e_pegar()
        if(blockPosition == 3 or blockPosition == 1):
            goToSquareSide(myDirection, EAST, esquerda)
            myDirection = NORTH
            blockNumber = identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = alinhar_cubo_na_direita_e_pegar()  
    if(((currentPosition == 34 or currentPosition== 44) and blockSquare < 4) or currentPosition == 37 or currentPosition == 47):
        if(blockPosition == 1 or blockPosition == 0):
            goToSquareSide(myDirection, NORTH, esquerda)
            myDirection = WEST
            blockNumber = identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = alinhar_cubo_na_direita_e_pegar()
        if(blockPosition == 3 or blockPosition == 2):
            goToSquareSide(myDirection, SOUTH, direita)
            myDirection = WEST
            blockNumber = identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = alinhar_cubo_na_esquerda_e_pegar()

    return myDirection, cube, blockNumber

    
            

def winOPEN():
    # initialPosition = 11
    inicio_virar_SUL()
    initialPosition = firstSq.identifyFirstPos(clientID)
    if(initialPosition[1] == -1):
        MoveSquareForward()
    iniY, iniX = firstSq.identifyFirstPos(clientID)
    initialPosition = (iniY+1)*10+(iniX+1)
    initialDirection = SOUTH

    currentPosition, myDirection, order, matrix = getBlocksInformation(initialPosition, initialDirection)
    #time.sleep(1000)
    #order = [1, 2, 3]
    pickLater = []
    blockZero = []
    #APENAS TESTE
    #order = gb.get_path(gb.createGraphBlocks(matrix))
    #currentPosition = initialPosition
    #myDirection = initialDirection
    #FIM DE TESTE
    n = len(order)
    for i in range(n):
        #blockLocalPickup, blockLocalDelivery, blockColor, hiddenBlock, blockPosition, blockSquare = course(order[i] - 2, matrix) #AQUI FUNCIONA COM O CODIGO SIMPLES!!!!!
        order, matrix = solvePath(matrix, currentPosition)
        matrix = np.delete(matrix, order[0], axis=0)
        blockLocalPickup, blockLocalDelivery, blockColor, hiddenBlock, blockPosition, blockSquare = course(order[0], matrix)
        print(blockLocalPickup, blockLocalDelivery, blockColor, hiddenBlock, blockPosition)
        if (not hiddenBlock):
            myDirection, currentPosition = firstCorrection(i, myDirection, currentPosition, blockLocalPickup)
            currentPosition, myDirection = goFromTo(currentPosition, blockLocalPickup, myDirection)
            myDirection, cube, blockNumber = grabBlock(currentPosition, blockPosition, myDirection, blockColor, blockSquare, )
            print(currentPosition, myDirection, cube, blockNumber)
            if(blockNumber == 0):
                abrir_garra()
                fechar_garra_total()
                abrir_garra()
                fechar_garra_total()
                abrir_garra()
                fechar_garra_total()
                blockZero.append([blockSquare, blockPosition])
            if((blockColor == 'K' or blockColor == 'W') and blockNumber != 0):
                #identifica número
                 ##### MODIFICAR QUANDO IDENTIFICAR
                if(currentPosition > 50):
                    currentPosition, myDirection = goFromTo(currentPosition, 44, myDirection)
                currentPosition, myDirection = goToShelfDeliver(blockNumber, currentPosition, myDirection, cube)
            elif(blockColor == 'R' or blockColor == 'G' or blockColor == 'B' or blockColor == 'Y'):
                currentPosition, myDirection = goFromTo(currentPosition, blockLocalDelivery, myDirection)
                entregar_cubo_colorido(cube)
        else:
            pickLater.append([blockColor, blockLocalPickup, blockLocalDelivery, blockSquare, blockPosition])
    for i in range(len(pickLater)):
        blockColor = pickLater[i][0]
        blockLocalPickup = pickLater[i][1]
        blockLocalDelivery = pickLater[i][2]
        blockSquare = pickLater[i][3]
        blockPosition = pickLater[i][4]
        blockLocalPickup = courseLastBlocks(blockSquare, blockPosition, blockZero, blockLocalPickup)
        currentPosition, myDirection = goFromTo(currentPosition, blockLocalPickup, myDirection)
        myDirection, cube, blockNumber = grabBlock(currentPosition, blockPosition, myDirection, blockColor, blockSquare) #### modificar para casos islolados
        andar_em_metros(tras, 3, 0.05)
        AlignBack(3)
        if((blockColor == 'K' or blockColor == 'W') and blockNumber != 0):
            if(currentPosition > 50):
                currentPosition, myDirection = goFromTo(currentPosition, 44, myDirection)
            currentPosition, myDirection = goToShelfDeliver(blockNumber, currentPosition, myDirection, cube)
        elif(blockColor == 'R' or blockColor == 'G' or blockColor == 'B' or blockColor == 'Y'):
            currentPosition, myDirection = goFromTo(currentPosition, blockLocalDelivery, myDirection)
            entregar_cubo_colorido(cube)








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
    erro, robo = sim.simxGetObjectHandle(clientID, 'S_Base', sim.simx_opmode_blocking)
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
    #currentPosition, myDirection = goFromTo(initialPosition, 32, initialDirection)
    #time.sleep(5)
    # while True:
    #     print(getColor(color_sensor_Left), getColor(color_sensor_Right))
    #     time.sleep(1)
    #Align()
    winOPEN()
    #print(find_initial_position())
    #abrir_garra()
    #Align()
    #alinhar_cubo_na_direita_e_pegar()
    # for i in range(5):
    #     MoveSquareForward()
    #getBlocksInformation(initialPosition, initialDirection)
    #TurnDirectionAng(direita, 90)
    # # time.sleep(10)
    # currentPosition, myDirection = goFromTo(initialPosition, 32, initialDirection)
    # print('cheguei pra pegar cubo')
    # currentPosition, myDirection = goFromTo(currentPosition, 14, myDirection)
    # currentPosition, myDirection = goToShelfDeliver(8, currentPosition, myDirection)
    # MoveDirectionPosition(tras, 0.01)
    # alinhar_cubo_na_direita_e_pegar()
    # currentPosition, myDirection = goFromTo(currentPosition, 71, myDirection)
    # entregar_cubo_colorido()
    # descer_elevador()
    # abrir_garra()
    # erro, cube = sim.simxGetObjectHandle(clientID, 'Cuboid6', sim.simx_opmode_blocking)
    # fechar_garra_cubo(cube)
    # #leave(cube)
    # #time.sleep(5)
   
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




