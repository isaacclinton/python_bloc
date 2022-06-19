from .bloc_observer import BlocObserver
from .bloc import Bloc
import threading


class TestObserver(BlocObserver):

    def __init__(self):
        super().__init__()
        self.states = []
        self.states_lock = threading.Lock()

    def on_change(self, old_state, new_state):
        super().on_change(old_state, new_state)
        self.states_lock.acquire()
        self.states.append(new_state)
        self.states_lock.release()


def bloc_test(*args, **kwargs):
    msg = args[0]
    assert type(msg) is str
    bloc = kwargs["bloc"]
    assert isinstance(bloc, Bloc)
    act_func = kwargs["act"]
    expect = kwargs["expect"]

    observer = TestObserver()
    bloc.set_observer(observer)

    act_func(bloc)
    if expect == observer.states:
        return True
    else:
        raise Exception(
            f"{msg}\nExpected: {[i for i in expect]}\nGot: {[i for i in observer.states]}"
        )