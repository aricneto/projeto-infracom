import socket


class Socket: 
    def __init__(self, sock=None, host="localhost", port=5000, buffer_size=1024, server=False):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock
        self.dest = (host, port)
        self.buffer_size = buffer_size
        
        if server: # se for um servidor, devemos chamar bind no endereço 
            self.sock.bind(self.dest)

    def sendUDP(self, msg):
        total_sent = 0
        MSGLEN = len(msg)
        while total_sent < MSGLEN: # enquanto a mensagem ainda não foi completamente enviada
            # parcelar a mensagem em pacotes tamanho buffer_size
            total_sent += self.sock.sendto(msg[total_sent:total_sent + self.buffer_size], self.dest)
            print(f"> Bytes enviados: {total_sent}")

    def receiveUDP(self):
        return self.sock.recvfrom(self.buffer_size)