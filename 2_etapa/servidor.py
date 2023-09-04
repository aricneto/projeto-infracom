from receiver import Receiver
from common import Socket
from os.path import join as pathjoin
import os.path

"""
Servidor UDP

"""


server = Receiver()

SERVER_DIR = "files_server"

# inicializar pasta server
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)


packet, address = None, []

while True:
    if packet is None:
        packet = server.wait_for_packet()
    else:
        print(f"Novo pacote: {packet}")
        
        if packet[:len(Socket.HEADER_START)] == Socket.HEADER_START:
            header = packet.split(",")
            print(f"Header recebido: {header}")
        packet = None


# server.sock.close()
