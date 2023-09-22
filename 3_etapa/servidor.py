from os.path import basename
from time import sleep
from datetime import datetime
from commands import Commands
from receiver import Receiver
from sender import Sender
from common import Socket
from utils import extract_msg_server
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

connected_users = {}

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

            receive_time = datetime.now().strftime('%H:%M:%S')

            # so enviar se souber de onde veio
            if g_address:
                msg = packet.decode()
                sender_address = g_address
                formatted_msg = ""


                sender_name, sender_msg = extract_msg_server(msg)

                # mostrar lista para quem requisitou
                if sender_msg == Commands.SHOW_LIST_CMD:
                    sender.rdt_send(f"Usuarios conectados: {connected_users}".encode(), sender_address)
                    packet = None
                    continue # prox loop

                # anunciar usuario
                if msg.endswith(Commands.USER_ENTERED):
                    formatted_msg = f"servidor: {msg}"
                    # adicionar usuario conectado
                    if sender_address not in connected_users:
                        sender_name = msg[:-len(Commands.USER_ENTERED)]
                        connected_users[sender_address] = sender_name

                # deslogar usuario
                elif sender_msg == Commands.LOGOUT_CMD:
                    if sender_address in connected_users:
                        del connected_users[sender_address]
                        formatted_msg = f"Usuario desconectado: {sender_name}"                

                # mensagem normal
                else:
                    formatted_msg = f"{sender_address[0]}:{sender_address[1]}/~{msg} <{receive_time}>"

                for client in receiver.clients:
                    if client != sender_address:
                        sender.rdt_send(formatted_msg.encode(), client)

            packet = None

main()