import unittest
from .counter_bloc import CounterBloc, Events
from src.bloc.bloc_test import bloc_test



class TestBloc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_counter(self):
        
        def act(bloc):
            bloc.add(Events.increment)
            bloc.add(Events.increment)
            bloc.add(Events.decrement)

        bloc_test(
            "Counter test",
            bloc=CounterBloc(),
            act=act,
            expect=[1, 2, 1],
        )
