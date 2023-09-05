from sender import Sender
from receiver import Receiver
from common import Socket
from os.path import basename
import os.path
import threading

"""
Cliente UDP

"""

client = Socket(port=1337)
sender = Sender(socket=client)
receiver = Receiver(socket=client)

# inicializar cliente

CLIENT_DIR = "files_client"
server_ip = "localhost"
server_port = 5000
server_address = (server_ip, server_port)
# inicializar pasta cliente
if not os.path.exists(CLIENT_DIR):
    os.makedirs(CLIENT_DIR)

def main():
    print ("Iniciando cliente...")

    send_thread = threading.Thread(target=send)

    send_thread.start()

    send_thread.join()

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
                filename = receiver.sock.receive_file(receiver=receiver, header=header, path=CLIENT_DIR)
                isReceivingFile = False
                break

            packet = None

def send():
    print ("Iniciando sender...")
    print("Bem vindo ao transmissor de mensagens 3000")

    comandos = [
        "Comandos disponiveis:",
        "- arquivo  | arq     : enviar arquivo",
        "- exit     | ext     : sair do programa",
        "- sdw                : desligar servidor",
    ]

    for comando in comandos:
        print(comando)

    msg = input("> ")

    while True:
        msg = input("> ")

        match msg:
            case "t" | "test":
                sender.sock.send_file(sender=sender, port=5000, msg="abisiildisn")
            case "exit" | "\x18" | "ext":
                break
            case "arq" | "arquivo":
                filename = input("> Digite o nome do arquivo:\n> ")
                match filename:
                    case "cheems":
                        filename = "../test_files/cheems.png"
                    case "dec":
                        filename = "../test_files/declaration.txt"
                    case "short":
                        filename = "../test_files/short.txt"
                    case "empty":
                        filename = "../test_files/empty.txt"
                try:
                    # enviar o arquivo
                    with open(filename, "rb") as f:
                        sender.sock.send_file(
                            sender=sender,
                            port=5000,
                            msg=f.read(),
                            filename=basename(filename)
                        )

                except IOError:
                    print("Nome de arquivo inválido!")

                # receber arquivo de volta
                receive()
                print ("Arquivo recebido de volta")

                
            case _:
                sender.rdt_send(msg, server_address)

main()