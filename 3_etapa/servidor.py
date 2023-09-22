from os.path import basename
from time import sleep
from receiver import Receiver
from sender import Sender
from common import Socket
import socket
from os.path import join as pathjoin
import os.path
import threading

"""
Servidor UDP

"""

server = Socket(port=5000)
receiver = Receiver(socket=server)
sender = Sender(socket=server)

g_address = None

SERVER_DIR = "files_server"

# inicializar pasta server
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)

def main():
    listen_thread = threading.Thread(target=listen)
    rcv_thread = threading.Thread(target=receive)
    
    listen_thread.start()
    rcv_thread.start()
    
    listen_thread.join()
    rcv_thread.join()

def listen():
    while True:
        header, packet, address = server.rdt_rcv()
        global g_address
        g_address = address
        
        sender.incoming_pkt = (header, packet, address)
        receiver.incoming_pkt = (header, packet, address)

def receive():
    print ("Iniciando receiver...")
    global g_address

    packet, address = None, []
    isReceivingFile = False
    header = ""

    while True:
        if packet is None:
            packet = receiver.wait_for_packet()
        else:
            print(f"Novo pacote: {packet}")
            print(f"from: {g_address}")

            original_sender = g_address
            for client in receiver.clients:
                if client != original_sender:
                    sender.rdt_send(packet, client)

            packet = None

main()