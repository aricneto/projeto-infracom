import socket
from enum import IntEnum


'''
Funções comuns a serem usadas pelos sockets

'''

class Socket: 
    HEADER_START = "HELLO"
    class Header(IntEnum):
        START = 0
        FILENAME = 1
        DATA_LENGTH = 2
        EXTRA = 3

    def __init__(self, sock=None, host="localhost", port=5000, buffer_size=1024, server=False):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock
        self.ip = (host, port)
        self.buffer_size = buffer_size
        
        if server: # se for um servidor, devemos chamar bind no endereço 
            self.sock.bind(self.ip)

    def sendUDP(self, msg=[], filename="", extra=""):
        # 1) calcular tamanho da mensagem em bytes
        MSGLEN = len(msg)
        total_sent = 0

        # 2) definir header da mensagem
        #                            ↱ nome do arquivo
        header = [self.HEADER_START, filename, str(MSGLEN), extra]
        #         ↳ identificador do header   |            ↳ mensagem extra
        #                                      ↳ tamanho da mensagem

        # 3) enviar header da mensagem
        print(f"Enviando um header de {len(header)} bytes")
        self.sock.sendto(",".join(header).encode(), self.ip)
        

        # 4) enviar mensagem parcelada em pacotes tamanho buffer_size
        print(f"Enviando um arquivo de {MSGLEN} bytes")
        while total_sent < MSGLEN: # enquanto a mensagem ainda não foi completamente enviada
            total_sent += self.sock.sendto(msg[total_sent:total_sent + self.buffer_size], self.ip)
            #print(f"> Bytes enviados: {total_sent}")

        if total_sent > 0 and total_sent == MSGLEN: 
            print(f"Arquivo enviado com sucesso: {filename}")

    def receiveUDP(self):
        return self.sock.recvfrom(self.buffer_size)
    
    # uma função de utilidade usada para esperar o recebimento de um header
    def receiveHeaderUDP(self):
        msg, _ = self.receiveUDP()

        if msg.decode()[:len(self.HEADER_START)] == self.HEADER_START:
            header = msg.decode().split(",")
            print(header)
            return header
        
        return None
        
    