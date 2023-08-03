from common import Socket
import re

"""
Servidor UDP

"""


server = Socket(server=True)

recebendo = False
header = ""

while True:
    if recebendo:
        server.sock.settimeout(5)
        filename = "output/output.txt"
        try:
            with open(filename, "wb") as new_file:
                msg_size = 0
                while True:
                    msg, _ = server.receiveUDP()
                    msg_size += len(msg)
                    new_file.write(msg)
                    
                    if msg_size == int(header[2]):
                        break
                print(f"Arquivo salvo: {filename}")
        except TimeoutError:
            print ("Erro na transmissão de arquivos.")
        server.sock.settimeout(None)
        recebendo = False

    if not recebendo:
        msg, _ = server.receiveUDP()

        if msg.decode()[:len(Socket.HEADER_START)] == Socket.HEADER_START:
            recebendo = True
            header = msg.decode().split(",")
            print(header)

        if msg.decode() == "sdw":
            break

server.sock.close()
