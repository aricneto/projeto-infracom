from os.path import splitext
import socket

'''
Funções comuns a serem usadas pelos sockets

'''

class Socket: 
    HEADER_START = "HELLO"
    HEADER_END = "END"
    HEADER_FILE = HEADER_START
    HEADER_MSG = HEADER_START + "type=message"
    FOOTER_END = "###### END OF FILE TRANSFER ######"

    def __init__(self, sock=None, host="localhost", port=5000, buffer_size=1024, server=False):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock
        self.ip = (host, port)
        self.buffer_size = buffer_size
        
        if server: # se for um servidor, devemos chamar bind no endereço 
            self.sock.bind(self.ip)

    def sendUDP(self, msg, filename=""):
        # 1) calcular tamanho da mensagem em bytes
        MSGLEN = len(msg)
        print(f"Enviando um arquivo de {MSGLEN} bytes")
        total_sent = 0

        # 2) enviar header da mensagem
        self.sock.sendto(",".join([self.HEADER_START, filename, str(MSGLEN)]).encode(), self.ip)
        #                          ↳ identificador do header
        #                                             ↳ nome do arquivo
        #                                                       ↳ tamanho da mensagem

        # 3) enviar mensagem parcelada em pacotes tamanho buffer_size
        while total_sent < MSGLEN: # enquanto a mensagem ainda não foi completamente enviada
            total_sent += self.sock.sendto(msg[total_sent:total_sent + self.buffer_size], self.ip)
            #print(f"> Bytes enviados: {total_sent}")
        print(f"Arquivo enviado: {filename}")

    def receiveUDP(self):
        return self.sock.recvfrom(self.buffer_size)