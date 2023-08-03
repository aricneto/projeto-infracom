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
                    client.sendUDP(f.read(), basename(filename))
            except IOError:
                print("Nome de arquivo inválido!")
        case "sdw":
            client.sendUDP(extra="sdw")
    
client.sock.close()
