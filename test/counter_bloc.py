from src.bloc import *
from enum import Enum


class Events(Enum):

    increment = 0
    decrement = 1


class CounterBloc(Bloc):

    def __init__(self, observer=None) -> None:
        super().__init__(0)
        self.on(Events.increment, self.__increment)
        self.on(Events.decrement, self.__decrement)

    def __increment(self, emit):
        emit(self.current_state() + 1)

    def __decrement(self, emit):
        emit(self.current_state() - 1)
