def find_initial_position():

    d=getDistanceIR(irRight)
    print(d)
    
    # se ele foi colocado virado pra prateleira => são os casos em q a posição inicial é: 12,22,13,23,15,25,16,26

    if(d!=1): 
        if(d<0.237141400576):
            l=1
        else:
            l=2
        AlignBack(3)
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
        a1=getColor(color_sensor_Right)
        b1=getColor(color_sensor_Left)

        if(a==VERDE or b==VERDE):

            if(a1==BRANCO or b1==BRANCO):
                andar_em_metros(tras,2,0.03)#testar valor
                TurnInSquare(90)
                return 71
            elif(a1==AZUL or b1==AZUL):
                andar_em_metros(tras,2,0.03)#testar valor
                TurnInSquare(90)
                return 77

        elif(a==AZUL or b==AZUL):
            
            if(a1==VERDE or b1==VERDE):
                andar_em_metros(tras,2,0.03)#testar valor
                TurnInSquare(90)
                return 72
            elif(a1==AMARELO or b1==AMARELO):
                andar_em_metros(tras,2,0.03)#testar valor
                TurnInSquare(90)
                return 76

        elif(a==AMARELO or b==AMARELO):
            
            if(a1==AZUL or b1==AZUL):
                andar_em_metros(tras,2,0.03)#testar valor
                TurnInSquare(90)
                return 73
            elif(a1==VERMELHO or b1==VERMELHO):
                andar_em_metros(tras,2,0.03)#testar valor
                TurnInSquare(90)
                return 75