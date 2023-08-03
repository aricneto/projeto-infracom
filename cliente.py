from common import Socket
from os.path import basename

"""
Cliente UDP

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
            client.sendUDP(mensagem.encode())
        case "arquivo" | "arq":
            filename = input("> Digite o nome do arquivo:\n> ")
            try:
                with open(filename, "rb") as f:
                    data = f.read()
                    client.sendUDP(data, basename(filename))
                    f.close()
            except IOError:
                print("Nome de arquivo inválido!")
        case "filesize" | "fsz":
            filename = "test_files/declaration.txt"
            with open(filename, "rb") as f:
                filesize = len(f.read())
                print(f"Bytes do arquivo: {filesize}")
        case "sdw":
            client.sendUDP("sdw".encode())
    
client.sock.close()
