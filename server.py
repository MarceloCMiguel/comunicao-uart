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
        print ("esperando receber handshake")
        list_handshake   =server.getDatagrams()
        
        print ("handshake chegou, enviando uma confirmação")
        list_datagrams=server.createDatagrams(bytes([10]))
        for packages in list_datagrams:
            server.sendDatagram(packages)
        recebeu_corretamente = False
        while recebeu_corretamente == False:
            list_package = server.getDatagrams()
            if list_package == False:
                print ("Erro na leitura de Datagrams, retornando mensagem de erro ao client")
                datagrams_error=server.createDatagrams(bytes([12]))
                for i in datagrams_error:
                    server.sendDatagram(i)
            else:
                recebeu_corretamente = True
        
        print ("package correto tudo certo, retornando mensagem de sucesso")
        time.sleep(2)

        datagrams_sucess = server.createDatagrams(bytes([11]))
        for i in datagrams_sucess:
            server.sendDatagram(i)
        file = b''.join(list_package)
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
