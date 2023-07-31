from common import Socket
from ntpath import basename

"""
Cliente UDP

Equipe: acn2
"""

client = Socket()
print("Bem vindo ao transmissor de mensagens 3000\nDigite CTRL+X para sair")
print("Comandos disponiveis:")
print("- arquivo  | arq     : enviar arquivo")
print("- mensagem | msg     : enviar mensagem")
print("- shutdown | sdw     : desligar servidor")
print("- exit     | ext     : sair do programa\n\n")

while True:
    msg = input("> ")

    match msg:
        case "exit" | "\x18" | "ext":
            break
        case "mensagem" | "msg":
            mensagem = input("> Digite sua mensagem:\n> ")
            # enviar mensagem com o header mensagem
            client.sendUDP((client.header("msg") + mensagem).encode())
        case "arquivo" | "arq":
            filename = input("> Digite o nome do arquivo:\n> ")
            try:
                with open(filename, "r") as f:
                    data = f.read()
                    # enviar mensagem com o header file, e o nome do arquivo
                    client.sendUDP((client.header("file", basename(filename)) + str(data)).encode())
                    f.close()
            except IOError:
                print("Nome de arquivo inválido!")

client.sock.close()
