from common import Socket

'''
Servidor UDP

Equipe: acn2
'''


server = Socket(server=True)

while True:
    msg, cliente = server.receiveUDP()

    print ("|", cliente, "| enviou |", msg.decode(), "|")
    
    if (msg.decode() == "shutdown"):
        break

server.sock.close()