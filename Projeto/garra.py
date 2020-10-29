# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

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

import time

#########################################

def MoveForward():
    vref = 1
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

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

def TurnLeft():
    vref=1
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, -vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

TERCEIRO_ANDAR = 0.12
SEGUNDO_ANDAR = 0.01
PRIMEIRO_ANDAR = -0.1

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
    sim.simxSetJointTargetPosition(clientID,paDireita,0.02,sim.simx_opmode_oneshot) 
    sim.simxSetJointTargetPosition(clientID,paEsquerda,0.02,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    time.sleep(1)

def pegar_cubo():
    abrir_garra()
    descer_elevador()
    fechar_garra()
    subir_elevador(SEGUNDO_ANDAR)

def entregar_cubo_colorido():
    descer_elevador()
    abrir_garra()
    subir_elevador(SEGUNDO_ANDAR)

def entregar_cubo_terceiro_andar():
    subir_elevador(TERCEIRO_ANDAR)
    #andar para frente certa quantidade
    abrir_garra()
    #andar para tras

def entregar_cubo_segundo_andar():
    subir_elevador(SEGUNDO_ANDAR)
    #andar para frente certa quantidade
    abrir_garra()
    #andar para tras

def entregar_cubo_primeiro_andar():
    subir_elevador(PRIMEIRO_ANDAR)
    #andar para frente certa quantidade
    abrir_garra()
    #andar para tras

def alinhar_cubo_na_esquerda_e_pegar():
    abrir_garra()
    descer_elevador()
    esquerda=0
    while True :
        a = getDistanceIR(irRight)
        b = getDistanceIR(irLeft)
        print(a,b)
        TurnLeft()
        if(b<1): 
            esquerda=esquerda+1
        if(a<1 and esquerda>0):
            break
    Stop()
    TurnRight()
    time.sleep(0.08)
    Stop()
    #andar pra frente certa quantidade
    #fechar_garra()
    #subir_elevador(SEGUNDO_ANDAR)

def alinhar_cubo_na_direita_e_pegar():
    abrir_garra()
    descer_elevador()
    direita=0
    while True :
        a = getDistanceIR(irRight)
        b = getDistanceIR(irLeft)
        print(a,b)
        TurnRight()
        if(a<1): 
            direita=direita+1
        if(b<1 and direita>0):
            break
    Stop()
    TurnLeft()
    time.sleep(0.08)
    Stop()
    #andar pra frente certa quantidade
    #fechar_garra()
    #subir_elevador(SEGUNDO_ANDAR)

    
######################################################


# MUDAR A CONFIGURACAO DOS CUBINHOS TODOS PRO ATRITO !!!!!!!!!!!!!!!!!!
# bug: ele ta andando pra tras.

# MAIN:

print ('Program started')
sim.simxFinish(-1) 
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID!=-1:
    print ('Connected to remote API server')


# HANDLES:
    erro,paEsquerda=sim.simxGetObjectHandle(clientID,'joint_pa_esquerda_garra',sim.simx_opmode_blocking)
    erro,paDireita=sim.simxGetObjectHandle(clientID,'joint_pa_direita_garra',sim.simx_opmode_blocking)
    erro,elevador=sim.simxGetObjectHandle(clientID,'joint_acoplador_garra',sim.simx_opmode_blocking)
    erro,irRight=sim.simxGetObjectHandle(clientID,'Sensor_IR_direito',sim.simx_opmode_blocking)
    erro,irLeft=sim.simxGetObjectHandle(clientID,'Sensor_IR_esquerdo',sim.simx_opmode_blocking)
    erro,robotLeftMotor=sim.simxGetObjectHandle(clientID,'Revolute_joint2',sim.simx_opmode_blocking)
    erro,robotRightMotor=sim.simxGetObjectHandle(clientID,'Revolute_joint1',sim.simx_opmode_blocking)
#

    #alinhar_cubo_na_direita_e_pegar()
    #alinhar_cubo_na_esquerda_e_pegar()


    sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)
    sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking )
    sim.simxFinish(clientID)

else:
    print ('Failed connecting to remote API server')
print ('Program ended')
