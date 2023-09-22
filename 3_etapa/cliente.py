from commands import Commands
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

username = None

def main():
    global username
    # login
    print(f"Bem vindo à sala de chat. Digite '{Commands.LOGIN_CMD}' para se conectar")
    
    while True: 
        msg = input()
        if msg.startswith(Commands.LOGIN_CMD):
            username = msg[len(Commands.LOGIN_CMD):]
            if len(username) > 0:
                break
    
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
            print(packet.decode())
            packet = None

def send():
    global username
    print (f"Bem vindo {username}!\n")

    greeting = f"{username}{Commands.USER_ENTERED}"
    sender.rdt_send(greeting, server_address)

    print (f"Digite sua mensagem!")

    while True:
        msg = input("")
        send_msg = f"{username}: {msg}"

        match msg:
            case s if s.startswith(Commands.ADD_FRIEND_CMD):
                friend = s[len(Commands.ADD_FRIEND_CMD):]
                print (f"add friend {friend}")
                pass
            case s if s.startswith(Commands.REMOVE_FRIEND_CMD):
                friend = s[len(Commands.REMOVE_FRIEND_CMD):]
                print (f"remove friend {friend}")
                pass
            case s if s.startswith(Commands.BAN_CMD):
                user = s[len(Commands.BAN_CMD):]
                print (f"ban user {user}")
                pass
            case s if s.startswith(Commands.SHOW_LIST_CMD):
                print (f"show list")
                pass
            case s if s.startswith(Commands.SHOW_FRIEND_LIST_CMD):
                print (f"show friend list")
                pass
            case s if s.startswith(Commands.LOGOUT_CMD):
                print ("Deslogado! Feche o terminal para sair")
                break
            case _:
                sender.rdt_send(send_msg, server_address)

main()