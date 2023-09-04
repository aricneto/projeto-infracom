from __future__ import annotations
from abc import ABC, abstractmethod
import threading
import time

from common import Socket
from utils import pretty_print

client = Socket()

# the sender class contains a _state that references the concrete state and setState method to change between states.
class Sender:
    SEND_PROBABILITY = 1

    def __init__(self, state=None) -> None:
        if state is not None:
            self.set_state(state)
        else:
            self.set_state(wait_for_call())

    def set_state(self, state: State):
        pretty_print(f"Sender: Mudando de estado para {type(state).__name__} seq={state.seq}")
        self._state = state
        self._state.sender = self

    def print_state(self):
        pretty_print(f"Sender esta em: {type(self._state).__name__} seq={self._state.seq}")
    
    def start_timer(self, duration=2):
        pretty_print("Iniciando temporizador", "*", "", "*")
        self._timer = threading.Timer(duration, self.timeout)
        self._timer.start()

    def stop_timer(self):
        pretty_print("Parando temporizador", "*", "", "*")
        self._timer.cancel()

    @property
    def sndpkt(self):
        return self._sndpkt
    
    @sndpkt.setter
    def sndpkt(self, sndpkt):
        self._sndpkt = sndpkt

    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, address):
        self._address = address

    def rdt_send(self, data):
        self._state.rdt_send(data)

    def rdt_rcv(self):
        self._state.rdt_rcv()
    
    def change_state(self, state: State):
        self._state.exit_action()
        self.set_state(state)
        self._state.entry_action()

    def timeout(self) -> None:
        print("Timeout, retransmitindo")
        client.udt_send(self._sndpkt, self._address, self.SEND_PROBABILITY)
        self.start_timer()


class State(ABC):

    def __init__(self, seq=0) -> None:
        self._seq = seq

    @property
    def seq(self):
        return self._seq

    @property
    def next_seq(self):
        return (self._seq + 1) % 2

    @property
    def sender(self) -> Sender:
        return self._sender

    @sender.setter
    def sender(self, sender: Sender) -> None:
        self._sender = sender

    @abstractmethod
    def rdt_send(self, data) -> None:
        pass

    @abstractmethod
    def rdt_rcv(self) -> bool:
        pass

    # Ação realizada pela maquina ao sair de um estado
    @abstractmethod
    def exit_action(self) -> None:
        pass

    # Ação realizada pela maquina ao entrar em um estado
    @abstractmethod
    def entry_action(self) -> None:
        pass

class wait_for_call(State):
    def __init__(self, seq=0) -> None:
        super().__init__(seq)

    def entry_action(self) -> None:
        return super().entry_action()
    
    def rdt_send(self, data) -> None:
        print (f"Sending: {data}")
        sndpkt = client.make_pkt(self.seq, data)

        # salvar pacote para retransmissao
        self.sender.sndpkt = sndpkt
        # salvar endereço para retransmissao
        self.sender.address = ("localhost", 5000)

        # enviar pacote
        client.udt_send(sndpkt, self.sender.address, self.sender.SEND_PROBABILITY)
        
        # iniciar temporizador
        self.sender.start_timer()

        # mudar estado
        self.sender.change_state(wait_for_ack(self.seq))
    
    def rdt_rcv(self) -> bool:
        return super().rdt_rcv()
    
    def exit_action(self) -> None:
        return super().exit_action()

class wait_for_ack(State):
    def __init__(self, seq=0) -> None:
        super().__init__(seq)

    def entry_action(self) -> None:
        while True:
            acked = self.rdt_rcv()

            if (acked):
                self.sender.change_state(wait_for_call(self.next_seq))
                break
    
    def rdt_send(self, data) -> None:
        return super().rdt_send(data)
    
    def rdt_rcv(self) -> bool:
        rcvpkt, _ = client.rdt_rcv()

        if rcvpkt and client.is_ACK(rcvpkt, self.seq):
            # pausar temporizador
            self.sender.stop_timer()
            return True 
        elif rcvpkt and client.is_ACK(rcvpkt, self.next_seq):
            return False
        else: # simular perda
            return False
        
    def exit_action(self) -> None:
        return super().exit_action()