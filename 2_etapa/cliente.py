from sender import Sender
from common import Socket
from os.path import basename
import os.path

"""
Cliente UDP

"""

# inicializar cliente
client = Sender()

CLIENT_DIR = "files_client"

# inicializar pasta cliente
if not os.path.exists(CLIENT_DIR):
    os.makedirs(CLIENT_DIR)


print("Bem vindo ao transmissor de mensagens 3000")

comandos = [
    "Comandos disponiveis:",
    "- arquivo  | arq     : enviar arquivo",
    "- exit     | ext     : sair do programa",
    "- sdw                : desligar servidor",
]

for comando in comandos:
    print(comando)

while True:
    msg = input("> ")

    match msg:
        case "t" | "test":
            client.rdt_send("abisuilson")
        case "exit" | "\x18" | "ext":
            break
        case _:
            print ("Digite um comando válido!")
            for comando in comandos:
                print(comando)

# client.sock.close()
