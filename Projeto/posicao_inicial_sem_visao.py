def find_initial_position():

    d=getDistanceIR(irRight)
    
    # se ele foi colocado virado pra prateleira => são os casos em q a posição inicial é: 12,22,13,23,15,25,16,26

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
            else if(a==AZUL or b==AZUL):
                andar_em_metros(tras,2,0.03)#testar valor
                return 77

        else if(a==AZUL or b==AZUL):
            
            if(a==VERDE or b==VERDE):
                andar_em_metros(tras,2,0.03)#testar valor
                return 72
            else if(a==AMARELO or b==AMARELO):
                andar_em_metros(tras,2,0.03)#testar valor
                return 76

        else if(a==AMARELO or b==AMARELO):
            
            if(a==AZUL or b==AZUL):
                andar_em_metros(tras,2,0.03)#testar valor
                return 73
            else if(a==VERMELHO or b==VERMELHO):
                andar_em_metros(tras,2,0.03)#testar valor
                return 75
            
