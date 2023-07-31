'''
Cliente UDP

Equipe: acn2
'''

from common import Socket


client = Socket()
print("Bem vindo ao transmissor de mensagens 3000\nDigite CTRL+X para sair")

while True:
    msg = input()

    # terminar o programa caso CTRL+X seja apertado
    if msg == "\x18": 
        break

    client.sendUDP(msg.encode())

client.sock.close()

