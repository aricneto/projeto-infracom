from sender import Sender
from receiver import Receiver
from common import Socket
from os.path import basename
import os.path
import threading
import random

"""
Cliente UDP

"""

client = Socket(port=random.randrange(3000, 8000))
sender = Sender(socket=client)
receiver = Receiver(socket=client)

# inicializar cliente
CLIENT_DIR = "files_client"

# definir servidor para onde vao ser enviados os arquivos
server_ip = "127.0.0.1"
server_port = 5000
server_address = (server_ip, server_port)

# inicializar pasta cliente
if not os.path.exists(CLIENT_DIR):
    os.makedirs(CLIENT_DIR)

def main():
    listen_thread = threading.Thread(target=listen)
    send_thread = threading.Thread(target=send)
    rcv_thread = threading.Thread(target=receive)
    
    listen_thread.start()
    send_thread.start()
    rcv_thread.start()
    
    listen_thread.join()
    send_thread.join()
    rcv_thread.join()
    

def listen():
    while True:
        header, packet, address = client.rdt_rcv()
        sender.incoming_pkt = (header, packet, address)
        receiver.incoming_pkt = (header, packet, address)

def receive():
    packet, address = None, []

    while True:
        if packet is None:
            packet = receiver.wait_for_packet()
        else:
            print(f"Novo pacote: {packet}")
            packet = None

def send():
    while True:
        msg = input("Digite um comando:  ")

        match msg:
            case "bye":
                break
            case _:
                sender.rdt_send(msg, server_address)

main()