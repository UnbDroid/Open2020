# coding=utf-8
# Insert in a script in Coppelia

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

from globalDefs import *
import globalDefs as glob


import math
import time
import numpy as np
import visionAlgo as vis
import giroAlgo as giro
import graphBlocksBetter as gbb
import firstSq
import locomAlgo as move
import logLocomAlgo as shift
import alignAlgo as align
import cuboAlgo as cubo
import garraAlgo as garra

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


### FUNÇÕES DESAFIO ###############################################################

def firstCorrection(i, myDirection, currentPosition, blockLocalPickup):
    #print(i, myDirection, currentPosition, blockLocalPickup)
    if(i == 0):
        if(currentPosition < 30):
            if(currentPosition % 10 > 4):
                if(blockLocalPickup % 10 >= 6):
                    print('east')
                    myDirection = shift.turnTo(myDirection, EAST, False)
                    currentPosition  = 26
                else:
                    print('west')
                    myDirection = shift.turnTo(myDirection, WEST, False)
                    currentPosition = 25
            else:
                if(blockLocalPickup % 10 > 2):
                    print('east')
                    myDirection = shift.turnTo(myDirection, EAST, False)
                    currentPosition = 23
                else:
                    print('west')
                    myDirection = shift.turnTo(myDirection, WEST, False)
                    currentPosition = 22
        else:
            if(currentPosition % 10 > 4):
                if(blockLocalPickup % 10 >= 6):
                    print('east')
                    myDirection = shift.turnTo(myDirection, EAST, False)
                    currentPosition  = 56
                else:
                    print('west')
                    myDirection = shift.turnTo(myDirection, WEST, False)
                    currentPosition = 55
            else:
                if(blockLocalPickup % 10 > 2):
                    print('east')
                    myDirection = shift.turnTo(myDirection, EAST, False)
                    currentPosition = 53
                else:
                    print('west')
                    myDirection = shift.turnTo(myDirection, WEST, False)
                    currentPosition = 52
        #andar_em_metros(frente, 5, 0.15)
        align.Align()
        print(currentPosition)
    return myDirection, currentPosition
	
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
    currentPosition, myDirection = shift.goFromTo(currentPosition, destine, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = shift.turnTo(myDirection ,direction, True)
    #Align() #TurnTo ja alinha
    move.andar_em_metros(frente, 2, 0.04)
    move.TurnDirectionAng(lastTurn, 90)
    myDirection = SOUTH
    align.Align()
    move.MoveDirectionPosition(tras, 0.065)
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
    currentPosition, myDirection = shift.goFromTo(currentPosition, destine, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = shift.turnTo(myDirection ,direction, True)
    #Align()
    move.andar_em_metros(frente, 2, 0.04)
    move.TurnDirectionAng(lastTurn, 90)
    myDirection = SOUTH
    align.Align()
    move.MoveDirectionPosition(tras, 0.065)
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
    currentPosition, myDirection = shift.goFromTo(currentPosition, destine, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = shift.turnTo(myDirection ,direction, True)
    #Align() #TurnTo ja alinha
    move.andar_em_metros(frente, 2, 0.04)
    move.TurnDirectionAng(lastTurn, 90)
    myDirection = NORTH
    align.Align()
    move.MoveDirectionPosition(tras, 0.065)
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
    currentPosition, myDirection = shift.goFromTo(currentPosition, destine, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = shift.turnTo(myDirection ,direction, True)
    #Align()
    move.andar_em_metros(frente, 2, 0.04)
    move.TurnDirectionAng(lastTurn, 90)
    myDirection = NORTH
    align.Align()
    move.MoveDirectionPosition(tras, 0.065)
    matrix1 = vis.resolveVision(clientID,1) #MODIFICAR MATRIZ
    matrix1 = gbb.invertMatrix(matrix1)
    return matrix1, currentPosition, myDirection

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

def getBlocksInformation(currentPosition, myDirection):
    print(currentPosition)
    if (currentPosition < 40): #Ta na parte de cima
        if(currentPosition % 10 <= 2):
            matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 1)
            #Vai para a segunda área
            myDirection = shift.turnTo(myDirection ,EAST, True)
            #MoveDirectionPosition(frente, 0.020)
            currentPosition += 1
            matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 2)
        elif(currentPosition % 10 <= 4):
            matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 2)
            #Vai para a segunda área
            myDirection = shift.turnTo(myDirection ,EAST, True)
            #MoveDirectionPosition(frente, 0.020)
            matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 2)
        else:
            matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 1)
            myDirection = shift.turnTo(myDirection ,WEST, True)
            currentPosition -= 1
            matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 2)
    else: #Ta na parte de baixo
        if(currentPosition % 10 <= 2):
            matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 1)
            #Vai para a segunda área
            myDirection = shift.turnTo(myDirection ,EAST, True)
            #MoveDirectionPosition(frente, 0.020)
            currentPosition += 1
            matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 2)
        elif(currentPosition % 10 <= 4):
            matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 2)
            #Vai para a segunda área
            myDirection = shift.turnTo(myDirection ,EAST, True)
            #MoveDirectionPosition(frente, 0.020)
            matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 2)
        else:
            matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 1)
            myDirection = shift.turnTo(myDirection ,WEST, True)
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
    #print(order, matrixFinal)
    

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


def grabBlock(currentPosition, blockPosition, myDirection, blockColor, blockSquare, hiddenBlock):
    print('grabBLock', currentPosition, blockPosition, myDirection, blockSquare)
    cube = glob.robo
    if(currentPosition == 22 or currentPosition== 23 or currentPosition == 25 or currentPosition == 26):
        if(blockPosition == 0 or blockPosition == 2):
            shift.goToSquareSide(myDirection, WEST, esquerda, hiddenBlock)
            myDirection = SOUTH
            blockNumber = cubo.identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = cubo.alinhar_cubo_na_direita_e_pegar()
        if(blockPosition == 1 or blockPosition == 3):
            shift.goToSquareSide(myDirection, EAST, direita, hiddenBlock)
            myDirection = SOUTH
            blockNumber = cubo.identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = cubo.alinhar_cubo_na_esquerda_e_pegar()
    if(currentPosition == 31 or currentPosition== 41 or ((currentPosition == 34 or currentPosition == 44) and (blockSquare > 3))):
        if(blockPosition == 0 or blockPosition == 1):
            shift.goToSquareSide(myDirection, NORTH, direita, hiddenBlock)
            myDirection = EAST
            blockNumber = cubo.identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = cubo.alinhar_cubo_na_esquerda_e_pegar()
        if(blockPosition == 2  or blockPosition == 3):
            shift.goToSquareSide(myDirection, SOUTH, esquerda, hiddenBlock)
            myDirection = EAST
            blockNumber = cubo.identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = cubo.alinhar_cubo_na_direita_e_pegar()
    if(currentPosition == 52 or currentPosition== 53 or currentPosition == 55 or currentPosition == 56):
        if(blockPosition == 2  or blockPosition == 0):
            shift.goToSquareSide(myDirection, WEST, direita, hiddenBlock)
            myDirection = NORTH
            blockNumber = cubo.identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = cubo.alinhar_cubo_na_esquerda_e_pegar()
        if(blockPosition == 3 or blockPosition == 1):
            shift.goToSquareSide(myDirection, EAST, esquerda, hiddenBlock)
            myDirection = NORTH
            blockNumber = cubo.identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = cubo.alinhar_cubo_na_direita_e_pegar()  
    if(((currentPosition == 34 or currentPosition== 44) and blockSquare < 4) or currentPosition == 37 or currentPosition == 47):
        if(blockPosition == 1 or blockPosition == 0):
            shift.goToSquareSide(myDirection, NORTH, esquerda, hiddenBlock)
            myDirection = WEST
            blockNumber = cubo.identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = cubo.alinhar_cubo_na_direita_e_pegar()
        if(blockPosition == 3 or blockPosition == 2):
            shift.goToSquareSide(myDirection, SOUTH, direita, hiddenBlock)
            myDirection = WEST
            blockNumber = cubo.identificar_valor(blockColor)
            if(blockNumber != 0):
                cube = cubo.alinhar_cubo_na_esquerda_e_pegar()

    return myDirection, cube, blockNumber

    
            

def winOPEN():
    move.inicio_virar_SUL()
    initialPosition = firstSq.identifyFirstPos(clientID)
    if(initialPosition[1] == -1):
        move.MoveSquareForward()
    iniY, iniX = firstSq.identifyFirstPos(clientID)
    initialPosition = (iniY+1)*10+(iniX+1)
    print(initialPosition)
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
        blockLocalPickup, blockLocalDelivery, blockColor, hiddenBlock, blockPosition, blockSquare = course(order[0], matrix)
        matrix = np.delete(matrix, order[0], axis=0)
        print(blockLocalPickup, blockLocalDelivery, blockColor, hiddenBlock, blockPosition)
        if (not hiddenBlock):
            myDirection, currentPosition = firstCorrection(i, myDirection, currentPosition, blockLocalPickup)
            currentPosition, myDirection = shift.goFromTo(currentPosition, blockLocalPickup, myDirection)
            myDirection, cube, blockNumber = grabBlock(currentPosition, blockPosition, myDirection, blockColor, blockSquare, hiddenBlock)
            print(currentPosition, myDirection, cube, blockNumber)
            if(blockNumber == 0):
                garra.abrir_garra()
                garra.fechar_garra_total()
                garra.abrir_garra()
                garra.fechar_garra_total()
                garra.abrir_garra()
                garra.fechar_garra_total()
                blockZero.append([blockSquare, blockPosition])
            if((blockColor == 'K' or blockColor == 'W') and blockNumber != 0):
                #identifica número
                 ##### MODIFICAR QUANDO IDENTIFICAR
                if(currentPosition > 50):
                    currentPosition, myDirection = shift.goFromTo(currentPosition, 44, myDirection)
                currentPosition, myDirection = shift.goToShelfDeliver(blockNumber, currentPosition, myDirection, cube)
            elif(blockColor == 'R' or blockColor == 'G' or blockColor == 'B' or blockColor == 'Y'):
                currentPosition, myDirection = shift.goFromTo(currentPosition, blockLocalDelivery, myDirection)
                cubo.entregar_cubo_colorido(cube)
        else:
            pickLater.append([blockColor, blockLocalPickup, blockLocalDelivery, blockSquare, blockPosition])
    for i in range(len(pickLater)):
        blockColor = pickLater[i][0]
        blockLocalPickup = pickLater[i][1]
        blockLocalDelivery = pickLater[i][2]
        blockSquare = pickLater[i][3]
        blockPosition = pickLater[i][4]
        blockLocalPickup = courseLastBlocks(blockSquare, blockPosition, blockZero, blockLocalPickup)
        currentPosition, myDirection = shift.goFromTo(currentPosition, blockLocalPickup, myDirection)
        myDirection, cube, blockNumber = grabBlock(currentPosition, blockPosition, myDirection, blockColor, blockSquare, True) #### modificar para casos islolados
        if(blockNumber == 0):
                garra.abrir_garra()
                garra.fechar_garra_total()
                garra.abrir_garra()
                garra.fechar_garra_total()
                garra.abrir_garra()
                garra.fechar_garra_total()
                blockZero.append([blockSquare, blockPosition])
        else:
            move.andar_em_metros(tras, 3, 0.05)
            align.AlignBack(3)
        if((blockColor == 'K' or blockColor == 'W') and blockNumber != 0):
            if(currentPosition > 50):
                currentPosition, myDirection = shift.goFromTo(currentPosition, 44, myDirection)
            currentPosition, myDirection = shift.goToShelfDeliver(blockNumber, currentPosition, myDirection, cube)
        elif(blockColor == 'R' or blockColor == 'G' or blockColor == 'B' or blockColor == 'Y'):
            currentPosition, myDirection = shift.goFromTo(currentPosition, blockLocalDelivery, myDirection)
            cubo.entregar_cubo_colorido(cube)








##########################################



print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
_clientID = sim.simxStart('127.0.0.1',19999,True,True,5000,5)
_robotname = 'Robot'

if _clientID != -1:
    glob.init(_clientID, _robotname)
    clientID = glob.clientID
    time.sleep(2)
    initialPosition = 11
    initialDirection = SOUTH

    winOPEN()

    # Pause simulation
    sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    # Now close the connection to V-REP:
    sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking )
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')




