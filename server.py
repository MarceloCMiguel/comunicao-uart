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
from datagram import *


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
                  # Windows(variacao de)
arduino2 = "COM2"
def main():
    try:
        #com2 = enlace(arduino2) 
        print("Habilitando comunicação:")
        #com2.enable()
        print("Comunicação habilitada!")
        print("-"*20) 
        server = datagram(arduino2)
        server.enable()
        ocioso =True
        while ocioso:
            print ("Servidor ocioso")
            print ("esperando receber handshake")
            handshake = server.getDatagrams()
            #Só tem um indice
            print (handshake)
            print ("Payload")
            print (handshake[10:-4])
            tipo_msg,sensor_id,server_id,n_total_pacotes,n_atual_pacote,handshake_ou_sizepayload, pacote_solicitado, ultimo_pacote_recebido, crc = server.classificaHead(handshake)
            print ("tipo de msg chega do handshake {}".format(tipo_msg))
            # Deve checkar o id, por enquanto n fiz ainda
            ocioso = False
            time.sleep(1)
        print ("handshake chegou, enviando uma confirmação")
        list_msg2 = server.createDatagrams(bytes([7])*10,tipo=2)
        print (list_msg2)
        server.sendDatagram(list_msg2[0])
        print ("Enviado msg2")
        time.sleep(1)
        cont = 1
        # numero qlqr no numpckg apenas para entrar no while, dentro do while chamo o valor correto
        numPckg = 2
        num_pckg_anterior= 0
        list_payload = []
        while cont <= numPckg:
            print("Cont: {}".format(cont))
            package = server.getOnTime(3)
            if package ==False:
                print ("Não recebemos nada, mandando msg tipo 5 e fechando")
                list_msg5 = server.createDatagrams(bytes([7])*10,tipo=5)
                server.sendDatagram(list_msg5[0])
                raise TypeError("Fechando server")
            else:
                tipo_msg,sensor_id,server_id,n_total_pacotes,n_atual_pacote,handshake_ou_sizepayload, pacote_solicitado, ultimo_pacote_recebido, crc = server.classificaHead(package)
                numPckg = n_total_pacotes
                print("Numero do packg anterior {}".format(num_pckg_anterior))
                print ("Numero atual do pacote: {}".format(n_atual_pacote))
                print ("NumPckg: {}".format(numPckg))
                if (n_atual_pacote - num_pckg_anterior == 1) and (tipo_msg==3) and (handshake_ou_sizepayload == len(package)-14):
                    print ("payload adicionado")
                    print (package[10:-4])
                    list_payload.append(package[10:-4])
                    list_msg4 = server.createDatagrams(bytes([7])*10,tipo=4,ultimo_pacote=n_atual_pacote)
                    server.sendDatagram(list_msg4[0])
                    print ("Recebido: {}/{}".format(cont,numPckg))
                    cont+=1
                    num_pckg_anterior =n_atual_pacote
                else:
                    print (":"*70)
                    list_msg6 = server.createDatagrams(bytes([7])*10, tipo=6,pacote_esperado=n_atual_pacote)
        file = b''.join(list_payload)
        print (file)
        print(len(list_payload))
        print ("Escrevendo a imagem")
        with open("assets/server/receive.png", "wb") as file2:
            file2.write(file)


        server.com.disable()
    except Exception as e:
        print (e)
        print("Occoreu um erro!")
        server.com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
