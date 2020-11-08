
def Girar_90_graus(d): 

    # d = 1 , anti horario, esquerda
    # d =-1 , horario, direita
    # v = velocidade
    v = 5
    g = 90

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
            if(abs(abs(gamma)-abs(gamma_inicial))>=0.02*g):
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
            if(abs(gamma-gamma_inicial)>=0.02*g):
                break
            sim.simxPauseCommunication(clientID, True)
            sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*0.4, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*0.4, sim.simx_opmode_oneshot)
            sim.simxPauseCommunication(clientID, False)
    Stop()


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

