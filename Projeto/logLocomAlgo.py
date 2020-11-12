# coding=utf-8
# Insert in a script in Coppelia

import sim
import globalDefs as glob
from globalDefs import *
import locomAlgo as move
import alignAlgo as align
import cuboAlgo as cubo

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
                    move.TurnInSquare(180)
                if(myDirection == WEST):
                    move.TurnInSquare(90)
                if(myDirection == EAST):
                    move.TurnInSquare(-90)
                return SOUTH
        if(movement < 0): #Quer ir pra cima (NORTE)
            if(myDirection == NORTH):
                return NORTH
            else:
                if(myDirection == SOUTH):
                    move.TurnInSquare(180)
                if(myDirection == WEST):
                    move.TurnInSquare(-90)
                if(myDirection == EAST):
                    move.TurnInSquare(90)
                return NORTH

    if(axis == axisY):
        if(movement > 0): #Quer ir pra direita (LESTE)
            if(myDirection == EAST):
                return EAST
            else:
                if(myDirection == WEST):
                    move.TurnInSquare(180)
                if(myDirection == NORTH):
                    move.TurnInSquare(-90)
                if(myDirection == SOUTH):
                    move.TurnInSquare(90)
                return EAST
        if(movement < 0): #Quer ir pra direita (OESTE)
            if(myDirection == WEST):
                return WEST
            else:
                if(myDirection == EAST):
                    move.TurnInSquare(180)
                if(myDirection == NORTH):
                    move.TurnInSquare(90)
                if(myDirection == SOUTH):
                    move.TurnInSquare(-90)
                return WEST

def turnTo(myDirection, finalDirection):
    if(finalDirection == NORTH):
        if(myDirection == EAST):
            move.TurnInSquare(90)
        if(myDirection == SOUTH):
            move.TurnInSquare(180)
        if(myDirection == WEST):
            move.TurnInSquare(-90)
        return NORTH
    if(finalDirection == EAST):
        if(myDirection == NORTH):
            move.TurnInSquare(-90)
        if(myDirection == SOUTH):
            move.TurnInSquare(90)
        if(myDirection == WEST):
            move.TurnInSquare(180)
        return EAST
    if(finalDirection == SOUTH):
        if(myDirection == EAST):
            move.TurnInSquare(-90)
        if(myDirection == NORTH):
            move.TurnInSquare(180)
        if(myDirection == WEST):
            move.TurnInSquare(90)
        return SOUTH
    if(finalDirection == WEST):
        if(myDirection == EAST):
            move.TurnInSquare(180)
        if(myDirection == SOUTH):
            move.TurnInSquare(-90)
        if(myDirection == NORTH):
            move.TurnInSquare(90)
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
        move.MoveSquareForward()
        myDirection = correctDirection(myDirection, +1, axisX)
        move.MoveSquareForward()
        currentPosition = 31
    if(currentPosition == 23):
        myDirection = correctDirection(myDirection, +1, axisY)
        move.MoveSquareForward()
        myDirection = correctDirection(myDirection, +1, axisX)
        move.MoveSquareForward()
        currentPosition = 34
    if(currentPosition == 25):
        myDirection = correctDirection(myDirection, -1, axisY)
        move.MoveSquareForward()
        myDirection = correctDirection(myDirection, +1, axisX)
        move.MoveSquareForward()
        currentPosition = 34
    if(currentPosition == 26):
        myDirection = correctDirection(myDirection, +1, axisY)
        move.MoveSquareForward()
        myDirection = correctDirection(myDirection, +1, axisX)
        move.MoveSquareForward()
        currentPosition = 37
    #Parte de baixo
    if(currentPosition == 52):
        myDirection = turnTo(myDirection, WEST)
        move.MoveSquareForward()
        myDirection = turnTo(myDirection, NORTH)
        move.MoveSquareForward()
        currentPosition = 41
    if(currentPosition == 53):
        myDirection = turnTo(myDirection, EAST)
        move.MoveSquareForward()
        myDirection = turnTo(myDirection, NORTH)
        move.MoveSquareForward()
        currentPosition = 44
    if(currentPosition == 55):
        myDirection = turnTo(myDirection, WEST)
        move.MoveSquareForward()
        myDirection = turnTo(myDirection, NORTH)
        move.MoveSquareForward()
        currentPosition = 44
    if(currentPosition == 56):
        myDirection = turnTo(myDirection, EAST)
        move.MoveSquareForward()
        myDirection = turnTo(myDirection, NORTH)
        move.MoveSquareForward()
        currentPosition = 47

    return currentPosition, myDirection


def goFromTo(currentPosition, finalPosition, myDirection):
    finalPosition = realFinalPosition(finalPosition)
    while(not arrived(currentPosition, finalPosition)):
        moveX = (finalPosition/10) - (currentPosition/10)
        moveY =  (finalPosition%10) - (currentPosition%10)
        if(moveY != 0 and notStockLocal(currentPosition, moveY, axisY)):
            myDirection = correctDirection(myDirection, moveY, axisY)
            move.MoveSquareForward()
            if(moveY > 0): #robô andou para a direita
                currentPosition += 1
            else: #robô andou para a esquerda
                currentPosition -= 1
        elif(moveX != 0 and notStockLocal(currentPosition, moveX, axisX)):
            myDirection = correctDirection(myDirection, moveX, axisX)
            move.MoveSquareForward()
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
        goToSquareSide(myDirection, EAST, esquerda, False)
        align.AlignSpecial(2)
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
        cubo.entregar_cubo_primeiro_andar(cube)
    elif(block <= 10):
        cubo.entregar_cubo_segundo_andar(cube)
    elif(block <= 15):
        cubo.entregar_cubo_terceiro_andar(cube)
    Prateleiras[block] += 1

    return currentPosition, myDirection


def goToSquareSide(myDirection, firstDirection, finalTurn, hiddenBlock):
    #move.MoveDirectionPosition(tras, 0.01)
    if(myDirection == -firstDirection):
    #if(False):
        move.andar_em_metros(tras, 5, 0.10)
        align.AlignBack(2)
        move.andar_em_metros(frente, 2, 0.16)
        move.TurnDirectionAng(-finalTurn, 90)
    else:
        print('virando', firstDirection)
        turnTo(myDirection, firstDirection)
        align.Align()
        move.MoveDirectionPosition(tras, 0.002)
        print('virando', finalTurn)
        move.TurnDirectionAng(finalTurn, 90)

    align.AlignSpecial(2)
    if not hiddenBlock:
        move.andar_em_metros(tras, 5, 0.06)

    #move.MoveDirectionPosition(tras, 0.01)
