from common import Socket
from os.path import join as pathjoin
import re

"""
Servidor UDP

"""


server = Socket(server=True)

recebendo = False
header = ""

while True:
    if recebendo and header:
        server.sock.settimeout(5)
        filename = pathjoin("output", header[Socket.Header.FILENAME])
        try:
            with open(filename, "wb") as new_file:
                msg_size = 0
                while True:
                    msg, _ = server.receiveUDP()
                    msg_size += len(msg)
                    new_file.write(msg)
                    
                    # parar quando tiver recebido todos os bytes especificados no header
                    if msg_size == int(header[Socket.Header.DATA_LENGTH]):
                        break
                print(f"Arquivo salvo: {filename}")
        except TimeoutError:
            print ("Erro no recebimento do arquivo")
        server.sock.settimeout(None)
        recebendo = False

    if not recebendo:
        header = server.receiveHeaderUDP()

        if header:
            recebendo = True

        if header and header[Socket.Header.EXTRA] == "sdw":
            break

server.sock.close()
