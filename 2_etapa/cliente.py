from sender import Sender
from common import Socket
from os.path import basename
import os.path

"""
Cliente UDP

"""

client = Sender()

def main():

    # inicializar cliente

    CLIENT_DIR = "files_client"
    server_ip = "localhost"
    server_port = 5000
    server_address = (server_ip, server_port)

    # inicializar pasta cliente
    if not os.path.exists(CLIENT_DIR):
        os.makedirs(CLIENT_DIR)


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
                client.sock.send_file(sender=client, port=5000, msg="abisiildisn")
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
                try:
                    # enviar o arquivo
                    with open(filename, "rb") as f:
                        client.sock.send_file(
                            sender=client,
                            port=5000,
                            msg=f.read(),
                            filename=basename(filename)
                        )

                except IOError:
                    print("Nome de arquivo inválido!")
            case _:
                client.rdt_send(msg, server_address)

main()