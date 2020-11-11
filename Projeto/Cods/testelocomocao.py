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
    erro, robot = sim.simxGetObjectHandle(clientID, robotname, sim.simx_opmode_oneshot_wait)
    #[erro, target] = sim.simxGetObjectHandle(clientID, targetname, sim.simx_opmode_oneshot_wait)
    [erro, robotLeftMotor] = sim.simxGetObjectHandle(clientID, 'Front_l_joint',sim.simx_opmode_oneshot_wait)
    [erro, robotRightMotor] = sim.simxGetObjectHandle(clientID, 'Front_r_joint', sim.simx_opmode_oneshot_wait)
    [erro, robotLeftMotorB] = sim.simxGetObjectHandle(clientID, 'Back_l_joint',sim.simx_opmode_oneshot_wait)
    [erro, robotRightMotorB] = sim.simxGetObjectHandle(clientID, 'Back_r_joint', sim.simx_opmode_oneshot_wait)

    # Criar stream de dados
    [erro, positionrobot] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_streaming)
    #[erro, positiontarget] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_streaming)
    [erro, orientationrobot] = sim.simxGetObjectOrientation(clientID,robot,-1,sim.simx_opmode_streaming)
    time.sleep(2)

    # Comandos motores
    vref = 1.0
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotorB, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotorB, vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    cont = 0
    while(cont < 8000):
        cont+=1
        # Coletar dados robôs e alvos
        [erro, [xr,yr,zr]] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_buffer)
        #[erro, [xt,yt,zt]] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_buffer)
        [erro, [alpha, beta, gamma]] = sim.simxGetObjectOrientation(clientID, robot, -1, sim.simx_opmode_buffer)

        
        sim.simxAddStatusbarMessage(clientID, 'A posição em x é '+str(xr) + ' e a posição em y é '+str(yr), sim.simx_opmode_oneshot_wait)

        

    # Stop simulation:
    # sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot_wait)

    # Pause simulation
    vref=0
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotRightMotorB, vref, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, robotLeftMotorB, vref, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)
    sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    # Now close the connection to V-REP:
    sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking )
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
