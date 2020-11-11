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

import sim
import time

## Setters
def init(_clientID, robotname):
	global robot, robo, robotLeftMotor, robotRightMotor
	global clientID
	global paEsquerda, paDireita
	global elevador, irRight, irLeft
	global color_sensor_Left, color_sensor_Right
	global positionrobot, angLeft, angRight, orientationrobot

	clientID = _clientID

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

	erro, angLeft = sim.simxGetJointPosition(clientID, robotLeftMotor, sim.simx_opmode_streaming)
	erro, angRight = sim.simxGetJointPosition(clientID, robotRightMotor, sim.simx_opmode_streaming)
	[erro, orientationrobot] = sim.simxGetObjectOrientation(clientID,robot,-1,sim.simx_opmode_streaming)

	sim.simxReadProximitySensor(clientID, irRight, sim.simx_opmode_streaming)
	sim.simxReadProximitySensor(clientID, irLeft, sim.simx_opmode_streaming)
	sim.simxGetVisionSensorImage(clientID, color_sensor_Left, 0, sim.simx_opmode_streaming)
	sim.simxGetVisionSensorImage(clientID, color_sensor_Right, 0, sim.simx_opmode_streaming)
