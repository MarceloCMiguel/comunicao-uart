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
        print("Esperando receber o tamanho da imagem")
        list_packages = []
        chegou_tamanho = False
        contador = 1
        while chegou_tamanho == False:
            rxBuffer, nRx = self.com.getData(10)
            print ("head recebido")
            print ("-"*20)
            # 2 bytes id
            # 2 bytes n_pacotes
            # 4 bytes size
            # 2 tipo de mensagem
            ID_bytes = rxBuffer[0:2]
            n_pacotes_bytes = rxBuffer[2:4]
            size_bytes= rxBuffer[4:8]
            msg_bytes = rxBuffer[8:10]

            n_pacotes = int.from_bytes(n_pacotes_bytes, byteorder='big')
            size = int.from_bytes(size_bytes, byteorder='big')
            ID = int.from_bytes(ID_bytes,byteorder='big')
            if contador != ID:
                print ("Erro nos pacotes")
                print("Enviando Resposta de erro")
                return False
            contador +=1
            package,nRx = self.com.getData(size)
            print ("package recebido")
            print ("-"*20)
            list_packages.append(package)
            eop,nRx = self.com.getData(4)
            print ("eop recebido")
            print ("-"*20)
            print ("Pacotes {}/{}".format(len(list_packages),n_pacotes))
            if len(list_packages) == n_pacotes:
                chegou_tamanho = True
        return list_packages


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

        

    def createDatagrams(self,content):
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
        
        # numero de pacotes em bytes
        n_pacotes_to_bytes = n_pacotes.to_bytes(2,'big')
        
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
        numero_eop = 309
        eop = numero_eop.to_bytes(4,'big')
        for size in lista_size:
            head = ID.to_bytes(2,'big') +n_pacotes_to_bytes + size.to_bytes(4,'big') + mensagem.to_bytes(2,'big')
            #ID +=1
            payout = content[contador:contador+size]
            contador +=size
            diagrama = head + payout + eop
            list_diagrams.append(diagrama)
        return list_diagrams
