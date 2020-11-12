
def cubo_proximo(): 

    descer_elevador()
    fechar_garra_total()   
      
    a=getDistanceIR(irRight)
    b=getDistanceIR(irLeft)

    if(a==1):
        distancia=b
        c="b"
    elif(b==1):
        distancia=a
        c="a"    
    elif(a!=1 and b!=1):
        if(a<b):
            distancia=a
            c="a"
        else:
            distancia=b
            c="b"

    if(distancia>=0.08): 
        valor= False #longe
    else: 
        valor= True #perto

    #print(c,distancia,valor)

    return valor

