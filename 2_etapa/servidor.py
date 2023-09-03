from common import Socket
from os.path import join as pathjoin
import os.path

"""
Servidor UDP

"""


server = Socket(port=5000, server=True)

SERVER_DIR = "files_server"

# inicializar pasta server
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)


packet, address = None, []

while True:
    if packet is None:
        packet, address = server.rdt_rcv()

    else:
        packet = None


server.sock.close()
