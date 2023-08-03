from common import Socket
from ntpath import basename

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
            client.sendUDP(client.header("msg").encode())
            client.sendUDP(mensagem.encode())
        case "arquivo" | "arq":
            filename = "test_files/declaration.txt"#input("> Digite o nome do arquivo:\n> ")
            try:
                with open(filename, "rb") as f:
                    data = f.read()
                    # enviar mensagem com o header file, nome do arquivo, e filesize
                    client.sendUDP(client.header("file", basename(filename), len(data)).encode())
                    client.sendUDP(data)
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
