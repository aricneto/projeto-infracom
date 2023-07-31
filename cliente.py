from common import Socket

"""
Cliente UDP

Equipe: acn2
"""

client = Socket()
print("Bem vindo ao transmissor de mensagens 3000\nDigite CTRL+X para sair")
print("Comandos disponiveis:")
print("> arquivo  | arq     : enviar arquivo")
print("> mensagem | msg     : enviar mensagem")
print("> shutdown | sdw     : desligar servidor")
print("> exit     | ext     : sair do programa\n\n")

while True:
    msg = input("> ")

    match msg:
        case "exit" | "\x18" | "ext":
            break
        case "mensagem" | "msg":
            mensagem = input("Digite sua mensagem:\n")
            client.sendUDP(mensagem.encode())
        case "arquivo" | "arq":
            filename = input("Digite o nome do arquivo:\n")
            try:
                arquivo = open(filename, "r")
                data = arquivo.read()
                if not data:
                    break
                while data:
                    client.sendUDP(str(data).encode())
                    data = arquivo.read()
                arquivo.close()
            except IOError:
                print("Nome de arquivo inválido!")

client.sock.close()
