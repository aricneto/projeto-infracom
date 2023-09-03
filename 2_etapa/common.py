import socket
from enum import IntEnum
from os.path import join as pathjoin
from os.path import basename

'''
Funções comuns a serem usadas pelos sockets

'''

class Socket: 
    HEADER_START = "HELLO"

    # define as posições de cada um dos elementos do header de uma transferência
    class Header(IntEnum):
        START = 0
        FILENAME = 1
        DATA_LENGTH = 2
        EXTRA = 3

    class PacketHeader(IntEnum):
        START = 0
        SEQ = 1
        DATA = 2

    def __init__(self, sock=None, ip="localhost", port=5000, buffer_size=1024, server=False):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock
        self.ip = (ip, port)
        self.buffer_size = buffer_size

        if server:
            self.sock.bind(self.ip)
            

    def sendUDP(self, port, ip="localhost", msg=[], filename="", extra=""):
        # 1) calcular tamanho da mensagem em bytes
        MSGLEN = len(msg)
        total_sent = 0
        destination = (ip, port)

        # 2) definir header da mensagem
        #                            ↱ nome do arquivo
        header = [self.HEADER_START, filename, str(MSGLEN), extra]
        #         ↳ identificador do header   |            ↳ mensagem extra
        #                                      ↳ tamanho da mensagem

        # 3) enviar header da mensagem
        print(f"Enviando um header de {len(header)} bytes")
        self.sock.sendto(",".join(header).encode(), destination)

        # 4) enviar mensagem parcelada em pacotes tamanho buffer_size
        print(f"Enviando um arquivo de {MSGLEN} bytes")
        while total_sent < MSGLEN: # enquanto a mensagem ainda não foi completamente enviada
            total_sent += self.sock.sendto(msg[total_sent:total_sent + self.buffer_size], destination)
            #print(f"> Bytes enviados: {total_sent}")

        if total_sent > 0 and total_sent == MSGLEN: 
            print(f"Arquivo enviado com sucesso: {filename}")

    def receiveUDP(self):
        return self.sock.recvfrom(self.buffer_size)
    
    # Espera o recebimento de um header
    def receiveHeaderUDP(self):
        msg, address = self.receiveUDP()

        if msg.decode()[:len(self.HEADER_START)] == self.HEADER_START:
            header = msg.decode().split(",")
            print(f"Header recebido: {header}")
            return (header, address)
        
        return (None, address)
        
    # recebe e salva um arquivo segundo as especificações de um header
    def receiveFileUDP(self, header, path="output", append=""):
        # enquanto estamos recebendo, aplicamos um timeout de 5 segundos (ver README)
        self.sock.settimeout(5)
        filename = pathjoin(path, append + header[Socket.Header.FILENAME])
        try:
            with open(filename, "wb") as new_file:
                msg_size = 0
                while True:
                    msg, _ = self.receiveUDP()
                    msg_size += len(msg)
                    new_file.write(msg)
                    
                    # parar quando tiver recebido todos os bytes especificados no header
                    if msg_size == int(header[Socket.Header.DATA_LENGTH]):
                        break
                print(f"Arquivo salvo: {filename}")
        except TimeoutError:
            print ("Erro no recebimento do arquivo")
        # desligar o timeout
        self.sock.settimeout(None)
        return basename(filename)
    
    def make_pkt(self, seq, data):
        # 1) definir header da mensagem
        #                            ↱ bit 'seq' do pacote
        msg = [self.HEADER_START, seq]
        #         ↳ identificador do header

        # 2) calcular tamanho do header em bytes
        HEADERLEN = len(msg)

        if len(data) + HEADERLEN > self.buffer_size:
            raise Exception ("Pacote não pode ser maior do que buffer_size")
        
        # 3) adicionar mensagem ao pacote
        msg.append(data)

        # 4) enviar mensagem
        ",".join(msg).encode()
