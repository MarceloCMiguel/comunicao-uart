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



# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
arduino1 = "COM5"                  # Windows(variacao de)
arduino2 = "COM6"
def main():
    try:
        start = time.time()
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        print("Estabelecendo enlace:")
        com1 = enlace(arduino1)
        com2 = enlace(arduino2)
        print("Enlace estabelecido com sucesso!")

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        print("Habilitando comunicação:")
        com1.enable()
        com2.enable()
        print("Comunicação habilitada!")
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        with open("assets/image_test.png", "rb") as file1:
            txBuffer = file1.read()


        # print("Enviando buffer: %s" %str(txBuffer))


        #txBuffer = imagem em bytes!
    

    
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        
    
            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        com1.sendData(txBuffer)

        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
    
       
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        
        rxBuffer, nRx = com2.getData(len(txBuffer))
        
        time.sleep(0.001)


        with open("assets/receive.png", "wb") as file2:
            file2.write(rxBuffer)
    
        
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        com2.disable()
        final = time.time()
        #delta t
        duracao = final - start
        vel=len(txBuffer)/duracao
        print ("Duração da transferência de imagem: {}".format(duracao))
        print ("Tamanho da imagem = {}".format(len(txBuffer)))
        print ("Velocidade de transferência da imagem: {} bytes/segundo".format(vel))
    except Exception:
        print (Exception)
        print("Occoreu um erro!")
        com1.disable()
        com2.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
