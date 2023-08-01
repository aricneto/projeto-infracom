from common import Socket
import re

'''
Servidor UDP

Equipe: acn2
'''


server = Socket(server=True)

contador = 0
recebido = ""

while True:
    msg, cliente = server.receiveUDP()
    
    recebido += msg.decode()


    print ("|", cliente, "| enviou |", msg.decode(), "|")

    # arquivo inteiro recebido
    if (recebido[-len(Socket.FOOTER_END):] == Socket.FOOTER_END):
        print("\n\nArquivo recebido por completo!")
        
        filename = 'output/output.txt'

        headerless = re.sub(r'\AHELLO \[FILE\] filename=.* END', '', recebido)
        with open(filename, "wb") as new_file:
            new_file.write(recebido.encode())
    
    if (msg.decode() == server.header("msg") + "shutdown" + Socket.FOOTER_END):
        break
    
server.sock.close()