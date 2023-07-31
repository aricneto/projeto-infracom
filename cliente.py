'''
Cliente UDP

Equipe: acn2
'''

import socket

class MySocket: 
    def __init__(self, sock=None, host="localhost", port=5000):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock
        self.dest = (host, port)
    
    

client = MySocket()

print("Bem vindo ao transmissor de mensagens 3000\nDigite CTRL+X para sair")


while True:
    msg = input()

    # terminar o programa caso CTRL+X seja apertado
    if msg == "\x18": 
        break

    client.sock.sendto(msg.encode(), client.dest)

client.sock.close()

