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
import logging

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
        logging.basicConfig(filename='client_1.log', filemode='w', format='CLIENT - %(asctime)s - %(message)s', level=logging.INFO)
        
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        print("Estabelecendo enlace:")
        client = datagram(arduino1)
        print("Enlace estabelecido com sucesso!")

        client.enable()
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        
        # HandShake
        valor_handshake = bytes([7])*10
        inicia = False
        while inicia == False:
            list_handshake = client.createDatagrams(valor_handshake,1)
            client.sendDatagram(list_handshake[0])
            logging.info("ENVIADO | TIPO: 1 | TAMANHO: {}".format(len(valor_handshake)+14))
            print ("handshake enviado, esperando confirmação")
            print("-"*20)
            confirmacao = client.getOnTime(5)
            if confirmacao == False:
                print ("não chegou")
            else:
                print ("package recebidooooo")
                print ("-"*20)
                tipo_msg,sensor_id,server_id,n_total_pacotes,n_atual_pacote,handshake_ou_sizepayload, pacote_solicitado, ultimo_pacote_recebido, crc = client.classificaHead(confirmacao)
                logging.info("RECEBIDO | TIPO: {} | TAMANHO: {}".format(tipo_msg,len(confirmacao)))
                if tipo_msg == 2:
                    logging.info("RECEBIDO | TIPO: {} | TAMANHO: {}".format(tipo_msg,len(confirmacao)))
                    logging.info("COMEÇANDO A ENVIAR A IMAGEM")
                    print ("Recebeu mensagem t2, handshake feito")
                    inicia = True
                else:
                    print ("Tipo de msg recebido: {}".format(tipo_msg))
                    print ("Enviando handshake novamente")
                    logging.info("RECEBIDO | TIPO: {} | TAMANHO: {} | ENVIANDO NOVAMENTE HANDSHAKE".format(tipo_msg,len(confirmacao)))
                
        




        start = time.time()
        cont = 1
        with open("C:/Users/marce/Desktop/Insper/4 semestre/CamFis/Comunicação UART/assets/client/image_test.png", "rb") as file1:
            txBuffer = file1.read()
        #print (txBuffer)
        list_datagrams = client.createDatagrams(txBuffer,3)
        print ("Começando a enviar o arquivo")
        print (len(list_datagrams))
        while cont <= len(list_datagrams):
            
            # Enviou um package da lista
            client.sendDatagram(list_datagrams[cont-1])
            logging.info("ENVIADO | TIPO: 3 | TAMANHO: {} | PACOTES ENVIADOS: {}/{}".format(len(list_datagrams[cont-1]), cont, len(list_datagrams)))

            print ("Esperando uma resposta, tempo de 20 segundos")
            package_resposta = client.getOnTime(20)
            if package_resposta == False:
                print ("Não recebemos nenhuma resposta")
                list_msg5 = client.createDatagrams(bytes([8])*10,5)
                client.sendDatagram(list_msg5[0])
                logging.info("ENCERRANDO COMUNICAÇÃO POR FALTA DE RESPOSTA DO SERVER")
                logging.info("ENVIADO | TIPO: {} | TAMANHO: {}".format(5,len(list_msg5[0])))
                raise TypeError("Fechando server")
            else:
                tipo_msg,sensor_id,server_id,n_total_pacotes,n_atual_pacote,handshake_ou_sizepayload, pacote_solicitado, ultimo_pacote_recebido, crc = client.classificaHead(package_resposta)
                print("tipo_msg recebido: {}".format(tipo_msg))
                if tipo_msg == 4:
                    logging.info("RECEBIDO | TIPO: {} | TAMANHO: {} | CRC: {} | ULTIMO PACOTE RECEBIDO PELO SERVIDOR: {}".format(tipo_msg,len(package_resposta),crc,ultimo_pacote_recebido))
                    print ("Enviado: {}/{}".format(cont,len(list_datagrams)))
                    cont +=1
                else:
                    logging.info("RECEBIDO | TIPO: {} | TAMANHO: {} | CRC: {} | PACOTE SOLICITADO: {}".format(tipo_msg,len(package_resposta),crc,pacote_solicitado))
                    logging.info("ENVIANDO PACOTE NOVAMENTE")
                    print ("Mandando novamente")
                    #volta pro começo do while
        logging.info("TODOS OS PACOTES ENVIADOS, ENCERRANDO COMUNICAÇÃO")
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
