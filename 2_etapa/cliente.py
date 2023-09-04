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
                sendUDP(port=5000, msg="abisiildisn")
            case "exit" | "\x18" | "ext":
                break
            case "arq" | "arquivo":
                filename = input("> Digite o nome do arquivo:\n> ")
                match filename:
                    case "cheems":
                        filename = "../test_files/cheems.png"
                    case "dec":
                        filename = "../test_files/declaration.txt"
                try:
                    # enviar o arquivo
                    with open(filename, "rb") as f:
                        sendUDP(
                            port=5000,
                            msg=f.read(),
                            filename=basename(filename),
                        )

                except IOError:
                    print("Nome de arquivo inválido!")
            case _:
                client.rdt_send(msg)

def sendUDP(port, ip="localhost", msg=[], filename="", extra=""):
        # 1) calcular tamanho da mensagem em bytes
        MSGLEN = len(msg)
        total_sent = 0
        destination = (ip, port)

        # 2) definir header da mensagem
        #                            ↱ nome do arquivo
        header = [Socket.HEADER_START, filename, str(MSGLEN), extra]
        #         ↳ identificador do header   |            ↳ mensagem extra
        #                                      ↳ tamanho da mensagem

        # 3) enviar header da mensagem
        print(f"Enviando um header de {len(header)} bytes")
        client.rdt_send(",".join(header))

        # 4) enviar mensagem parcelada em pacotes tamanho buffer_size
        print(f"Enviando um arquivo de {MSGLEN} bytes")
        while total_sent < MSGLEN: # enquanto a mensagem ainda não foi completamente enviada
            next_sent = total_sent + 1024 - client.sock.HEADERLEN()
            client.rdt_send(msg[total_sent:next_sent])
            total_sent = next_sent
            #print(f"> Bytes enviados: {total_sent}")

        if total_sent > 0 and total_sent == MSGLEN: 
            print(f"Arquivo enviado com sucesso: {filename}")
# client.sock.close()

main()