from common import Socket
import re

"""
Servidor UDP

Equipe: acn2
"""


server = Socket(server=True)

contador = 0
recebido = ""
recebendo = False
header = ""

while True:
    msg, cliente = server.receiveUDP()

    if recebendo:
        recebido += msg.decode()

    if not recebendo and msg.decode()[:len(Socket.HEADER_START)] == Socket.HEADER_START:
        recebendo = True
        header = msg.decode()

    print("|", cliente, "| enviou |", msg.decode(), "|")

    # arquivo inteiro recebido
    if recebendo and recebido[-len(Socket.FOOTER_END) :] == Socket.FOOTER_END:
        print(f"\n\nArquivo recebido por completo!\nHeader: {header}")

        filename = "output/output.txt"

        recebido = recebido[: -len(Socket.FOOTER_END)]
        with open(filename, "w") as new_file:
            new_file.write(recebido)

        recebendo = False
        recebido = ""

    if msg.decode() == server.header("msg") + "shutdown" + Socket.FOOTER_END:
        break

server.sock.close()
