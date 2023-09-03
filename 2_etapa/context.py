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
            self.set_state(wait_for_call_0())

    def set_state(self, state: State):
        print(f"Sender: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.sender = self

    def print_state(self):
        print(f"Sender esta em: {type(self._state).__name__}")

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

class wait_for_call_0(State):
    def entry_action(self) -> None:
        return super().entry_action()
    
    def rdt_send(self, data) -> None:
        sndpkt = client.make_pkt(0, data)
        self.sender.set_sndpkt(sndpkt)
        client.sock.sendto(sndpkt, ("localhost", 5000))
        # todo: start_timer
        self.sender.change_state(wait_for_ack_0())
    
    def rdt_rcv(self) -> bool:
        return super().rdt_rcv()
    
    def exit_action(self) -> None:
        return super().exit_action()

class wait_for_ack_0(State):
    def entry_action(self) -> None:
        while True:
            acked = self.rdt_rcv()

            if (acked):
                self.sender.change_state(wait_for_call_1())
    
    def rdt_send(self, data) -> None:
        return super().rdt_send(data)
    
    def rdt_rcv(self) -> bool:
        rcvpkt, address = client.rdt_rcv()
        if rcvpkt and client.isACK(rcvpkt, 0):
            # todo: stop timer
            return True 
        if rcvpkt and client.isACK(rcvpkt, 1):
            return False
        else: 
            # timeout
            client.sock.sendto(self.sender.get_sndpkt(), ("localhost", 5000))
            return False
        
    
    def exit_action(self) -> None:
        return super().exit_action()

class wait_for_call_1(State):
    def entry_action(self) -> None:
        return super().entry_action()
    def exit_action(self) -> None:
        return super().exit_action()
    def rdt_rcv(self) -> bool:
        return super().rdt_rcv()
    def rdt_send(self, data) -> None:
        return super().rdt_send(data)