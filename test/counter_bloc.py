from src.bloc import *
from enum import Enum


class Events(Enum):

    increment = 0
    decrement = 1


class CounterBloc(Bloc):

    def __init__(self) -> None:
        super().__init__(0)
        self.on(Events.increment, self.__increment)
        self.on(Events.decrement, self.__decrement)

    def __increment(self, event, emit):
        emit(self.current_state() + 1)

    def __decrement(self, event, emit):
        emit(self.current_state() - 1)
