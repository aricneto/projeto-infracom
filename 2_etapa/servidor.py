from os.path import basename
from time import sleep
from receiver import Receiver
from sender import Sender
from common import Socket
from os.path import join as pathjoin
import os.path
import threading

"""
Servidor UDP

"""

server = Socket(port=5000)
receiver = Receiver(socket=server)
sender = Sender(socket=server)

SERVER_DIR = "files_server"

# inicializar pasta server
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)

def main():
    print ("Iniciando servidor...")
    receive()


def receive():
    print ("Iniciando receiver...")

    packet, address = None, []
    isReceivingFile = False
    header = ""

    while True:
        if packet is None:
            packet = receiver.wait_for_packet()
        else:
            print(f"Novo pacote: {packet}")

            if not isReceivingFile and packet[:len(Socket.HEADER_START)] == Socket.HEADER_START.encode():
                header = packet.decode().split(",")
                isReceivingFile = True
                print(f"Header recebido: {header}")
            if isReceivingFile:
                filename = receiver.sock.receive_file(receiver=receiver, header=header, path=SERVER_DIR)
                isReceivingFile = False
                sleep(1)
                print ("Enviando de volta")
                # Enviar de volta
                with open(filename, "rb") as f:
                        sender.sock.send_file(
                            sender=sender,
                            port=1337,
                            msg=f.read(),
                            filename=basename(filename)
                        )
                print ("Arquivo enviado de volta")

            packet = None

main()