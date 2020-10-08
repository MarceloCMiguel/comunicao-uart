#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import os
from datagram import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
arduino1 = "COM1"                  # Windows(variacao de)
def main():
    try:
        
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        print("Estabelecendo enlace:")
        client = datagram(arduino1)
        print("Enlace estabelecido com sucesso!")

        client.enable()
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        
        #datagram = datagram(com1)
        # HandShake
        valor_handshake = bytes([10])

        with open("C:/Users/marce/Desktop/Insper/4 semestre/CamFis/Client-Server/assets/client/image_test.png", "rb") as file1:
            txBuffer = file1.read()


        inicia = False
        while inicia == False:
            list_handshake = client.createDatagrams(valor_handshake,1)
            list_resposta_handshake = []
            recebeu_resposta = False
            print ("enviando handshake")
            print ("-"*20)
            while recebeu_resposta == False:
                for handshake in list_handshake:
                    client.sendDatagram(handshake)
                print ("handshake enviado, esperando confirmação")
                print("-"*20)
                confirmacao = client.com.getOnTime(10,5)
                if confirmacao == False:
                    resposta = input("Servidor inativo. Tentar novamente? S/N")
                    if resposta == "n":
                        raise TypeError("Fechando client")
                else:
                    print ("head recebido")
                    print ("-"*20)
                    # 2 bytes id
                    # 2 bytes n_pacotes
                    # 4 bytes size
                    # 2 tipo de mensagem
                    tipo_msg = int.from_bytes(confirmacao[0])
                    sensor_id = int.from_bytes(confirmacao[1])
                    server_id = int.from_bytes(confirmacao[2])
                    n_total_pacotes = int.from_bytes(confirmacao[3])
                    n_atual_pacote = int.from_bytes(confirmacao[4])
                    handshake_ou_sizepayload = int.from_bytes(confirmacao[5])
                    pacote_solicitado = int.from_bytes(confirmacao[6])
                    ultimo_pacote_recebido = int.from_bytes(confirmacao[7])
                    crc = int.from_bytes(confirmacao[8:10])
                    
                    package = client.com.getOnTime(10,5)
                    if package == False:
                        resposta = input("Servidor inativo. Tentar novamente? S/N")
                        if resposta == "n":
                            raise TypeError("Fechando client")
                    else:
                        print ("package recebido")
                        print ("-"*20)
                        list_resposta_handshake.append(package)
                        eop= client.com.getOnTime(4,5)
                        if eop == False:
                            resposta = input("Servidor inativo. Tentar novamente? S/N")
                            if resposta == "n":
                                raise TypeError("Fechando client")
                        else:
                            print ("eop recebido")
                            print ("-"*20)
                            print ("Handshake feito, tudo correto")
                            print ("n_pacotes_handshake {}".format(n_total_pacotes))
                            print ("list_packages_handshake {}".format(len(list_resposta_handshake)))
                            recebeu_resposta=True
                            inicia = True
        cont = 1
        with open("C:/Users/marce/Desktop/Insper/4 semestre/CamFis/Client-Server/assets/client/image_test.png", "rb") as file1:
            txBuffer = file1.read()
        list_datagrams = []
        list_datagrams = client.createDatagrams(txBuffer,3)
        while cont <= len(list_datagrams):
            # Enviou um package da lista
            client.sendDatagram(list_datagrams[cont-1])
            resposta = client.com.getOnTime(24,1)
            tipo_msg,sensor_id,server_id,n_total_pacotes,n_atual_pacote,handshake_ou_sizepayload, pacote_solicitado, ultimo_pacote_recebido, crc = client.classificaHead(resposta)
            if tipo_msg == 4:
                cont +=1
            elif tipo_msg == 5:
                pass





        # print ("Escolhendo a imagem")
        # folder_path = "C:/Users/marce/Desktop/Insper/4 semestre/CamFis/Fragmentação, hand-shake e datagrama/assets/client/"
        # os.listdir(folder_path)
        # print (os.listdir(folder_path))
        # lenpath = (len(os.listdir(folder_path)))
        # choice = int(input("Por favor, seleciona a posição da imagem  que deseja enviar (de 1 a {}): ".format(lenpath)))
        # file_path = os.path.join(folder_path, os.listdir(folder_path)[choice-1])

        # print ("Começando a gravar o tempo")
        # print ("-"*20)
        # start = time.time() 

        # print ("Lendo a imagem:")
        # print ("-"*20)
        # #Leitura da imagem
        with open(file_path, "rb") as file1:
            txBuffer = file1.read()
        list_datagrams = []
        list_datagrams = client.createDatagrams(txBuffer)
        print ("-"*20)
        recebeu_corretamente = False
        while recebeu_corretamente == False:
            for package in list_datagrams:
                client.sendDatagram(package)

            print ("Pacotes entregues, esperando resposta do servidor")
            response = client.getDatagrams()

            print ("Se retornar 11, tudo certo")
            print ("Se retornar 12, deu errado")
            file = b''.join(response)
            checkagem = int.from_bytes(file,byteorder='big')
            print ("Resposta do servidor: {}".format(checkagem))
            if checkagem == 11:
                recebeu_corretamente = True
                print("Pacotes enviados com sucesso, fechando client")
            else:
                print("Erro no pacote, enviando corretamente")
            # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        client.com.disable()
        final = time.time()
        #delta t
        duracao = final - start
        #vel=len(txBuffer)/duracao
    except Exception as e:
        print (e)
        print("Occoreu um erro!")
        client.disable()




    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
