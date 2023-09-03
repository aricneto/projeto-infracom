from __future__ import annotations
from abc import ABC, abstractmethod

from common import Socket

client = Socket(port=1337)

# the sender class contains a _state that references the concrete state and setState method to change between states.
class Sender:

    def __init__(self, state=None) -> None:
        if state is not None:
            self.set_state(state)
        else:
            self.set_state(wait_for_call())

    def set_state(self, state: State):
        print(f"Sender: Transitioning to {type(state).__name__} seq={state.seq}")
        self._state = state
        self._state.sender = self

    def print_state(self):
        print(f"Sender esta em: {type(self._state).__name__} seq={self._state.seq}")

    def set_sndpkt(self, sndpkt):
        self._sndpkt = sndpkt

    def get_sndpkt(self):
        return self._sndpkt

    def rdt_send(self, data):
        self._state.rdt_send(data)

    def rdt_rcv(self):
        self._state.rdt_rcv()
    
    def change_state(self, state: State):
        self._state.exit_action()
        self.set_state(state)
        self._state.entry_action()


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
        sndpkt = client.make_pkt(self.seq, data)
        self.sender.set_sndpkt(sndpkt)
        client.sock.sendto(sndpkt, ("localhost", 5000))
        # todo: start_timer
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
    
    def rdt_send(self, data) -> None:
        return super().rdt_send(data)
    
    def rdt_rcv(self) -> bool:
        rcvpkt, address = client.rdt_rcv()
        if rcvpkt and client.is_ACK(rcvpkt, self.seq):
            # todo: stop timer
            return True 
        if rcvpkt and client.is_ACK(rcvpkt, self.next_seq):
            return False
        else: 
            # timeout
            client.sock.sendto(self.sender.get_sndpkt(), address)
            return False
        
    
    def exit_action(self) -> None:
        return super().exit_action()