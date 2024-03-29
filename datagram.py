#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Interface Física
from interfaceFisica import fisica
import crcmod
# enlace Tx e Rx
from enlace import enlace

class datagram(object):
    
    def __init__(self, com):
        self.com      = enlace(com)
        

    def enable(self):
        print("Habilitando comunicação:")
        self.com.enable()
        print("Comunicação habilitada!")
        print ("-"*20)

    def disable(self):
        self.com.disable()
        

    def getDatagrams(self):
        # pedindo o head
        print("Esperando receber o handshake")
        rxBuffer,nRxBuffer = self.com.getData(10)
        
        
        tipo_msg = rxBuffer[0]
        sensor_id =rxBuffer[1]
        server_id = rxBuffer[2]
        n_total_pacotes =rxBuffer[3]
        n_atual_pacote = rxBuffer[4]
        handshake_ou_sizepayload = rxBuffer[5]
        pacote_solicitado = rxBuffer[6]
        ultimo_pacote_recebido = rxBuffer[7]
        crc = int.from_bytes(rxBuffer[8:10], byteorder='big')
        
        print ("head recebido")
        print ("-"*20)

        print ("Tipo da mensagem: {}".format(tipo_msg))
        if handshake_ou_sizepayload != 0:
            
            package,nRx = self.com.getData(handshake_ou_sizepayload)
        else:
            package,nRx = self.com.getData(10)
        print ("package recebido")
        print ("-"*20)
        #Comentei a linha que faz com que retorne apenas o payload, mais interessante pegar todas as infos
        #list_packages.append(package)
        eop,nRx = self.com.getData(4)
        print ("eop recebido")
        print ("-"*20)
        print ("Recebido o pacote de id {}".format(n_atual_pacote))
        pacote = rxBuffer + package + eop
        
        return pacote


    def sendDatagram(self,datagram):
        head = datagram[0:10]
        payout = datagram[10:-4]
        eop = datagram[-4:]
        print("enviando head")
        print("-"*20)
        self.com.sendData(head)
        time.sleep(0.1)
        print("enviando payout")
        print("-"*20)
        self.com.sendData(payout)
        time.sleep(0.1)
        print("enviando eop")
        print("-"*20)
        self.com.sendData(eop)
        time.sleep(0.1)

        

    def createDatagrams(self,content,tipo, ultimo_pacote = 0, pacote_esperado = 0):
        # Fazendo o head
        lista_size = []
        if len(content) > 114:
            tamanho = len(content)
            while tamanho >0:
                if tamanho>114:
                    lista_size.append(114)
                    tamanho = tamanho - 114
                else:
                    lista_size.append(tamanho)
                    tamanho = 0
            n_pacotes = len(lista_size)
        else:
            n_pacotes = 1
            lista_size.append(len(content))
        print ("Lista size")
        print (lista_size)
         # numero de pacotes em bytes
        n_pacotes_to_bytes = n_pacotes.to_bytes(1,'big')
        #Head
        h1 = 1
        h1 = h1.to_bytes(1,'big')
        h2 = 1
        h2 = h2.to_bytes(1,'big')
        h3 = n_pacotes_to_bytes
        h5 = 0
        # Vai aumentando no loop
        h4 = 1
        h6 = pacote_esperado.to_bytes(1,'big')
        h7 = ultimo_pacote.to_bytes(1,'big')
        crc16_func = crcmod.mkCrcFun(0x11021, initCrc=0, xorOut=0xFFFFFFFF) #armazena a funcao que faz o bagui
        if tipo==1:
            h2 = 1
            h2 = h2.to_bytes(1,'big')
        elif tipo == 3:
            #Coloquei esse numero para reconhecer dentro do for de baixo e mostrar que é do tipo 3
            h5 = 3
        h0 = tipo.to_bytes(1,'big')
        num = 255
        num2 = 170
        num1_tobytes = num.to_bytes(1,'big')
        num2_tobytes = num2.to_bytes(1,'big')
        #eop =: 0xFF 0xAA 0xFF 0xAA
        eop = num1_tobytes + num2_tobytes + num1_tobytes + num2_tobytes 
        
        # Criando heads e adicionando em uma lista de heads
        list_diagrams = []
        ID = 1
        #head
        # 2 bytes id
        # 2 bytes n_pacotes
        # 4 bytes size
        # 2 tipo de mensagem
        mensagem = 0
        contador = 0
        for size in lista_size:
            if h5 == 3:
                tamanho = size.to_bytes(1,'big')
            else:
                bla = 0
                tamanho = bla.to_bytes(1,'big')
            payload = content[contador:contador+size]
            crc_out = crc16_func(payload).to_bytes(2, "big")
            h4_to_bytes = h4.to_bytes(1,'big')
            head = h0+h1 + h2 + h3 + h4_to_bytes + tamanho + h6 + h7 + crc_out
            h4 +=1
            
            contador +=size
            diagrama = head + payload + eop
            list_diagrams.append(diagrama)
        return list_diagrams

    def classificaHead(self,head):
        tipo_msg = head[0]
        sensor_id = head[1]
        server_id = head[2]
        n_total_pacotes = head[3]
        n_atual_pacote = head[4]
        handshake_ou_sizepayload = head[5]
        pacote_solicitado = head[6]
        ultimo_pacote_recebido = head[7]
        crc = head[8:10]
        return tipo_msg,sensor_id,server_id,n_total_pacotes,n_atual_pacote,handshake_ou_sizepayload, pacote_solicitado, ultimo_pacote_recebido, crc

    def getOnTime(self,timer):
        # pedindo o head
        rxBuffer = self.com.getOnTime(10,timer)
        if rxBuffer == False:
            return False
        else:
            
            tipo_msg = rxBuffer[0]
            sensor_id =rxBuffer[1]
            server_id = rxBuffer[2]
            n_total_pacotes =rxBuffer[3]
            n_atual_pacote = rxBuffer[4]
            handshake_ou_sizepayload = rxBuffer[5]
            pacote_solicitado = rxBuffer[6]
            ultimo_pacote_recebido = rxBuffer[7]
            crc = int.from_bytes(rxBuffer[8:10], byteorder='big')
            
            print ("head recebido")
            print ("-"*20)

            print ("Tipo da mensagem: {}".format(tipo_msg))
            if handshake_ou_sizepayload != 0:
                print ("Esperando pacote de tamanho {}".format(handshake_ou_sizepayload))
                package,nRx = self.com.getData(handshake_ou_sizepayload)
            else:
                package,nRx = self.com.getData(10)
            print ("package recebido")
            print ("-"*20)
            #Comentei a linha que faz com que retorne apenas o payload, mais interessante pegar todas as infos
            #list_packages.append(package)
            eop,nRx = self.com.getData(4)
            print ("eop recebido")
            print ("-"*20)
            print ("Recebido o pacote de id {}".format(n_atual_pacote))
            pacote = rxBuffer + package + eop
            
            return pacote