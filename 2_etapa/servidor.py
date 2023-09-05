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
                receiveFileUDP(header, SERVER_DIR)
                isReceivingFile = False

            packet = None


def receiveHeaderUDP(self):
        msg, address = self.receiveUDP()
        print(msg.decode())

        if msg.decode()[:len(self.HEADER_START)] == self.HEADER_START:
            header = msg.decode().split(",")
            print(f"Header recebido: {header}")
            return (header, address)
        
        return (None, address)

def receiveFileUDP(header, path="output", append=""):
        # enquanto estamos recebendo, aplicamos um timeout de 5 segundos (ver README)
        filename = pathjoin(path, append + header[Socket.Header.FILENAME])
        try:
            with open(filename, "wb") as new_file:
                msg_size = 0
                while True:
                    msg = server.wait_for_packet()
                    msg_size += len(msg)
                    new_file.write(msg)
                    print (f"transferidos {msg_size} bytes")
                    # parar quando tiver recebido todos os bytes especificados no header
                    if msg_size == int(header[Socket.Header.DATA_LENGTH]):
                        print("transferencia completa")
                        break
                print(f"Arquivo salvo: {filename}")
        except TimeoutError:
            print ("Erro no recebimento do arquivo")
        # desligar o timeout
        return basename(filename)

main()