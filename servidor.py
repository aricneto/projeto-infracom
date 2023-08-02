from common import Socket
import re

"""
Servidor UDP

"""


server = Socket(server=True)

recebido = ""
recebendo = False
header = ""

while True:
    msg, cliente = server.receiveUDP()

    if recebendo:
        recebido += msg.decode()

    if not recebendo and msg.decode()[:len(Socket.HEADER_START)] == Socket.HEADER_START:
        recebendo = True
        header = msg.decode().split(",")
        print(header)

    print("|", cliente, "| enviou |", msg.decode(), "|")

    # arquivo inteiro recebido
    if recebendo and len(recebido) == int(header[2]):
        print(f"\n\nArquivo recebido por completo!\nHeader: {header}")

        filename = "output/output.txt"
        
        with open(filename, "w") as new_file:
            new_file.write(recebido)

        recebendo = False
        recebido = ""

    if not recebendo and msg.decode() == "sdw":
        break

server.sock.close()
