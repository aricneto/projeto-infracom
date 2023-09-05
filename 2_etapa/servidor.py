from os.path import basename
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

def main():
    packet, address = None, []
    isReceivingFile = False
    header = ""

    while True:
        if packet is None:
            packet = server.wait_for_packet()
        else:
            print(f"Novo pacote: {packet}")

            if not isReceivingFile and packet[:len(Socket.HEADER_START)] == Socket.HEADER_START.encode():
                header = packet.decode().split(",")
                isReceivingFile = True
                print(f"Header recebido: {header}")
            if isReceivingFile:
                server.sock.receive_file(receiver=server, header=header, path=SERVER_DIR)
                isReceivingFile = False

            packet = None

main()