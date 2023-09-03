from __future__ import annotations
from abc import ABC, abstractmethod

from common import Socket

client = Socket(port=5000, server=True)

# the sender class contains a _state that references the concrete state and setState method to change between states.
class Receiver:

    def __init__(self, state=None) -> None:
        if state is not None:
            self.set_state(state)
        else:
            self.set_state(wait_for_below())

    def set_state(self, state: State):
        print(f"Receiver: Transitioning to {type(state).__name__} seq={state.seq}")
        self._state = state
        self._state.receiver = self
        self._state.entry_action()

    def print_state(self):
        print(f"Receiver esta em: {type(self._state).__name__} seq={self._state.seq}")

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
    def receiver(self) -> Receiver:
        return self._receiver

    @receiver.setter
    def receiver(self, receiver: Receiver) -> None:
        self._receiver = receiver

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

class wait_for_below(State):
    def __init__(self, seq=0) -> None:
        super().__init__(seq)

    def entry_action(self) -> None:
        while True:
            acked = self.rdt_rcv()

            if (acked):
                self.receiver.change_state(wait_for_below(seq=self.next_seq))
                break
    
    def rdt_send(self, data) -> None:
        return super().rdt_send(data)
    
    def rdt_rcv(self) -> bool:
        rcvpkt, address = client.rdt_rcv()

        if rcvpkt and client.has_SEQ(rcvpkt, self.seq):
            print(f"has seq {self.seq}")
            # extract data
            # deliver data
            sndpkt = client.make_ack(self.seq)
            self.receiver.set_sndpkt(sndpkt)
            client.sock.sendto(sndpkt, address)
            return True
        elif rcvpkt and client.has_SEQ(rcvpkt, self.next_seq):
            print(f"has seq {self.next_seq}")
            sndpkt = client.make_ack(self.seq)
            self.receiver.set_sndpkt(sndpkt)
            client.sock.sendto(sndpkt, address)
            return False
        return False
    
    def exit_action(self) -> None:
        return super().exit_action()