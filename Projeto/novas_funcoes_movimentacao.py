# explicar o remendo.

    
# mudar as juntas pra velocidade.


# adicionar o handle:
erro, robo = sim.simxGetObjectHandle(clientID, 'S_Base', sim.simx_opmode_blocking)
    

# chamar na main:
andar_em_metros(1,5,0.3)
girar_90_graus(1,3)


# AS FUNÇÕES:

def andar_em_metros(d,v,m):
    
    # d = 1 , andar para frente
    # d =-1 , andar para trás
    # v = velocidade
    # m = valor em metros

    erro,a_inicial=sim.simxGetObjectPosition(clientID,robo,-1,sim.simx_opmode_blocking)
    x_inicial=a_inicial[0]
    y_inicial=a_inicial[1]
    while(True):
        erro,a=sim.simxGetObjectPosition(clientID,robo,-1,sim.simx_opmode_blocking)
        x=a[0]
        y=a[1]
        #print(x,y)
        if(abs(x-x_inicial)>=m or abs(y-y_inicial)>=m): 
            break 
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID, robotRightMotor,d*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(clientID, robotLeftMotor,d*v, sim.simx_opmode_oneshot)
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




