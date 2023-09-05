import random
import socket
from enum import IntEnum
from os.path import join as pathjoin
from os.path import basename

'''
Funções comuns a serem usadas pelos sockets

'''

class Socket: 
    HEADER_START = "HELLO"
    PACKET_START = "HELLOPKT"

    # define as posições de cada um dos elementos do header de uma transferência
    class Header(IntEnum):
        START = 0
        FILENAME = 1
        DATA_LENGTH = 2
        EXTRA = 3

    class PacketHeader(IntEnum):
        START = 0
        ACK = 1
        SEQ = 2
        DATA = 3

    def __init__(self, sock=None, ip="localhost", port=None, buffer_size=1024):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock

        self.buffer_size = buffer_size

        if port and ip:
            self.address = (ip, port)
            self.sock.bind(self.address)
            

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
    
    # Espera o recebimento de um pacote
    def rdt_rcv(self):
        msg, address = self.receiveUDP()

        if msg[:len(self.PACKET_START)].decode() == self.PACKET_START:
            header = msg[:self.HEADERLEN() - 1].decode().split(",")
            packet = msg[self.HEADERLEN() - 1:]
            print("\n### --- ###")
            print(f"# Pacote recebido: {header}")
            print(f"# seq={header[self.PacketHeader.SEQ]}, ack={header[self.PacketHeader.ACK]}")
            return (header, packet, address)
        
        return (None, None, address)
    
    # envia pacotes via UDP. simula perdas de acordo com @param probability
    def udt_send(self, data, address, probability=1.0):
        rand = random.random()
        print (f"Enviando: {data} para: {address}")
        if rand < probability:
            return self.sock.sendto(data, address)
        else:
            print("Simulando falha na transmissão!")
            return 0

    def HEADERLEN(self) -> int:
        return len(','.join([self.PACKET_START, "0", "0", "0"]))
    
    def make_pkt(self, seq, data, ack=0):
        # 1) definir header da mensagem
        #                            ↱ "bit" 'ack' do pacote
        msg = [self.PACKET_START, str(ack), str(seq)]
        #         ↳ identificador do header  ↳ "bit" 'seq' do pacote

        msg = ",".join(msg).encode()

        # 2) calcular tamanho do header em bytes
        HEADERLEN = len(msg)

        if data and len(data) + HEADERLEN > self.buffer_size:
            raise Exception ("Pacote não pode ser maior do que buffer_size")
        
        # 3) adicionar mensagem ao pacote
        if isinstance(data, bytes):
            msg = msg + b"," + data
        else:
            msg = msg + b"," + data.encode()

        print(f"\n\npacote: {msg[:HEADERLEN]}")
        # 4) criar pacote
        return msg
    
    def next_seq(self, seq):
        return (seq + 1) % 2
    
    def is_ACK(self, rcvpkt, seq):
        pkt_ack = int(rcvpkt[self.PacketHeader.ACK])
        pkt_seq = int(rcvpkt[self.PacketHeader.SEQ])
        print (f"> Check: is_ACK?")
        print (f"-> ack bit: {pkt_ack}")
        print (f"-> seq bit: {pkt_seq}, expected: {seq}")
        print (f"-> is_ACK: {pkt_ack == 1 and pkt_seq == seq}")
        return pkt_ack == 1 and pkt_seq == seq
    
    def has_SEQ(self, rcvpkt, seq):
        pkt_seq = int(rcvpkt[self.PacketHeader.SEQ])
        print (f"> Check: has_SEQ?")
        print (f"-> seq bit: {pkt_seq}, expected: {seq}")
        print (f"-> has_SEQ: {pkt_seq == seq}")
        return pkt_seq == seq
    
    def make_ack(self, seq):
        return self.make_pkt(seq=seq, data="", ack=1)
        
    # Espera o recebimento de um header
    def receiveHeaderUDP(self):
        msg, address = self.receiveUDP()
        print(msg.decode())

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
    
    
        
