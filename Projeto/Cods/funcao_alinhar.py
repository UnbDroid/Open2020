def Align():   #em desenvolvimento
    direita_preto = False
    esquerda_preto = False

    while(True):

        if (getColor(color_sensor_Left) == PRETO or getColor(color_sensor_Right) == PRETO):
            print("To procurando a linha")
            print("Achei pela primeira vez")
            break

        andar_livre(1, 5)

    Stop()
    [erro, pri_pos_cor_dir] = sim.simxGetObjectPosition(clientID, color_sensor_Right, -1, sim.simx_opmode_buffer)
    [erro, pri_pos_cor_esq] = sim.simxGetObjectPosition(clientID, color_sensor_Left, -1, sim.simx_opmode_buffer)

    if (getColor(color_sensor_Left) == PRETO):
        esquerda_preto = True

        while(True):

            if (getColor(color_sensor_Right) == PRETO):
                print("Achei pela segunda vez")
                break

            andar_livre(1, 5)

    elif (getColor(color_sensor_Right) == PRETO):
        direita_preto = True

        while(True):

            if (getColor(color_sensor_Left) == PRETO):
                print("Achei pela segunda vez")
                break

            andar_livre(1, 5)

    Stop()
    [erro, seg_pos_cor_dir] = sim.simxGetObjectPosition(clientID, color_sensor_Right, -1, sim.simx_opmode_buffer)
    [erro, seg_pos_cor_esq] = sim.simxGetObjectPosition(clientID, color_sensor_Left, -1, sim.simx_opmode_buffer)

    #A essa altura, o robô já andou, viu a linha com o primeiro sensor, andou mais e viu a linha com o segundo

    linha_vertical = False
    linha_horizontal = False

    x_p_dif_trans = np.abs(pri_pos_cor_dir[0] - pri_pos_cor_esq[0])
    x_s_dif_trans = np.abs(seg_pos_cor_dir[0] - seg_pos_cor_esq[0])
    x_e_dif_longi = np.abs(pri_pos_cor_esq[0] - seg_pos_cor_esq[0])
    x_d_dif_longi = np.abs(pri_pos_cor_dir[0] - seg_pos_cor_dir[0])

    y_p_dif_trans = np.abs(pri_pos_cor_dir[1] - pri_pos_cor_esq[1])
    y_s_dif_trans = np.abs(seg_pos_cor_dir[1] - seg_pos_cor_esq[1])
    y_e_dif_longi = np.abs(pri_pos_cor_esq[1] - seg_pos_cor_esq[1])
    y_d_dif_longi = np.abs(pri_pos_cor_dir[1] - seg_pos_cor_dir[1])


        ######################################################################
        ##### TABELA EXPLICATIVA #####
        #Essa tabela vale para x e para y, mas separadamente
        #S*n = "sensor" + lado (d=direita, e=esquerda) + vez que viu a linha (1a ou 2a)
        #dif = diferenca
        #trans = transversal (sempre compara direita e esquerda)
        #longi = longitudinal (sempre compara o mesmo lado)
        #cruz = cruzada (existe e eh diferente de zero, mas nao sera utilizada)
        #p = primeira (1a = 1), s = segunda (2a = 2)
        #
        #    |      SE1      |      SD1      |      SE2      |      SD2      |
        #SE1 |       0       |  p_dif_trans  |  e_dif_longi  | -ed_dif_cruz- |
        #SD1 |  p_dif_trans  |       0       | -de_dif_cruz- |  d_dif_longi  |
        #SE2 |  e_dif_longi  | -de_dif_cruz- |       0       |  s_dif_trans  |
        #SD2 | -ed_dif_cruz- |  d_dif_longi  |  s_dif_trans  |       0       |



    if(x_s_dif_trans > y_s_dif_trans):
        linha_horizontal = True

        if (esquerda_preto == True):

            if(y_e_dif_longi > 1):
                print("Estou descentralizado para a esquerda")
                #criar funcao que recentraliza
            else:
                while(True):

                    [erro, atual_pos_cor_esq] = sim.simxGetObjectPosition(clientID, color_sensor_Left, -1, sim.simx_opmode_buffer)
                    ye_atual_dif_longi = np.abs(seg_pos_cor_esq[1] - atual_pos_cor_esq[1])

                    if(int(ye_atual_dif_longi*1000000) >= int(y_s_dif_trans*1000000)):
                        print("Alinhando")
                        print("Alinhei")
                        print(int(ye_atual_dif_longi*100000))
                        print(int(y_s_dif_trans*100000))
                        break

                    gira_livre_uma_roda(esq, 1, 0.1)



        elif (direita_preto == True):

            if(y_d_dif_longi > 1):
                print("Estou descentralizado para a direita")
                #criar funcao que recentraliza
            else:
                while(True):

                    [erro, atual_pos_cor_dir] = sim.simxGetObjectPosition(clientID, color_sensor_Right, -1, sim.simx_opmode_buffer)
                    yd_atual_dif_longi = np.abs(seg_pos_cor_dir[1] - atual_pos_cor_dir[1])

                    if(int(yd_atual_dif_longi*1000000) >= int(y_s_dif_trans*1000000)):
                        print("Alinhando")
                        print("Alinhei")
                        print(int(yd_atual_dif_longi*1000000))
                        print(int(y_s_dif_trans*1000000))
                        break

                    gira_livre_uma_roda(dir, -1, 0.1)


    elif(x_s_dif_trans < y_s_dif_trans):
        linha_vertical = True

        if (esquerda_preto == True):

            if (x_e_dif_longi > 1):
                print("Estou descentralizado para a esquerda")
                # criar funcao que recentraliza
            else:
                while (True):

                    [erro, atual_pos_cor_esq] = sim.simxGetObjectPosition(clientID, color_sensor_Left, -1, sim.simx_opmode_buffer)
                    xe_atual_dif_longi = np.abs(seg_pos_cor_esq[0] - atual_pos_cor_esq[0])

                    if (int(xe_atual_dif_longi*1000000) >= int(x_s_dif_trans*1000000)):
                        print("Alinhando")
                        print("Alinhei")
                        print(int(xe_atual_dif_longi*1000000))
                        print(int(x_s_dif_trans*1000000))
                        break

                    gira_livre_uma_roda(esq, 1, 0.1)

        elif (direita_preto == True):

            if (x_d_dif_longi > 1):
                print("Estou descentralizado para a direita")
                # criar funcao que recentraliza
            else:
                while (True):

                    [erro, atual_pos_cor_dir] = sim.simxGetObjectPosition(clientID, color_sensor_Right, -1, sim.simx_opmode_buffer)
                    xd_atual_dif_longi = np.abs(seg_pos_cor_dir[0] - atual_pos_cor_dir[0])

                    if (int(xd_atual_dif_longi*1000000) >= int(x_s_dif_trans*1000000)):
                        print("Alinhando")
                        print("Alinhei")
                        print(xd_atual_dif_longi)
                        print(x_s_dif_trans)
                        break

                    gira_livre_uma_roda(dir, -1, 0.1)




    Stop()
    print("Parei de girar")

    if (getColor(color_sensor_Left) != PRETO):
        print("Esquerdo branco")
    else:  # (getColor(color_sensor_Right) == PRETO):
        print("Esquerdo preto")
    if (getColor(color_sensor_Right) != PRETO):
        print("Direito branco")
    else:  # (getColor(color_sensor_Left) == PRETO):
        print("Direito preto")
