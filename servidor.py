from common import Socket
from os.path import join as pathjoin
import re

"""
Servidor UDP

"""


server = Socket(server=True)

header = None

while True:
    if header is None:
        header = server.receiveHeaderUDP()

    else:
        # comando de debug para desligar o servidor remotamente
        if header[Socket.Header.EXTRA] == "sdw":
            break

        # receber o arquivo
        server.receiveFileUDP(header)
        # resetar o estado de header para receber outro arquivo
        header = None

        

server.sock.close()
