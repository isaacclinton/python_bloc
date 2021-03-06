import threading
from .bloc_observer import BlocObserver
from enum import Enum


class Bloc:

    def __init__(self, initial_state) -> None:
        self.__listeners = []
        self.__event_map = {}
        self.__event_queue = []
        self.__event_queue_lock = threading.RLock()  # using a reentrant lock, so that an event can be added while emit is taking place(on the same thread)
        self.__running_lock = threading.RLock()
        self.__observer = None
        self.__state = initial_state

    def current_state(self):
        return self.__state

    def on(self, event_type, process):
        if event_type in self.__event_map:
            raise Exception(f"{event_type} already registered")
        if not isinstance(event_type, Enum):
            event_type = event_type.__name__
        self.__event_map[event_type] = process

    def __emit(self, state):
        """
        will not emit if previous state and new state are the same
        """
        old_state = self.__state
        new_state = state
        should_emit = old_state != new_state
        if not should_emit:
            return
        self.__state = new_state
        if self.__observer is not None:
            self.__observer.on_change(old_state, new_state)
        for listener in self.__listeners:
            listener(state)

    def __execute_next_event(self):
        self.__running_lock.acquire()
        self.__event_queue_lock.acquire()
        if len(self.__event_queue) > 0:
            event = self.__event_queue[0]
            process = self.__event_map[event]

            process(event, self.__emit)

            # works fine most of the time without checking if the event_queue is empty
            # but just to make unsafe implementation doesn't cause IndexError while popping
            if len(self.__event_queue) > 0:
                self.__event_queue.pop(0)
        else:
            self.__event_queue_lock.release()
            self.__running_lock.release()
            return
        self.__event_queue_lock.release()
        self.__running_lock.release()
        self.__execute_next_event()

    def add(self, event):
        self.__event_queue_lock.acquire()
        if isinstance(event, Enum):
            self.__event_queue.append(event)
        else:
            self.__event_queue.append(event.__class__.__name__)
        self.__event_queue_lock.release()
        self.__execute_next_event()

    def set_observer(self, observer):
        assert isinstance(observer, BlocObserver)
        if self.__observer is not None:
            raise Exception("Observer already specified for the bloc")

        self.__observer = observer

    def listen(self, listener):
        self.__listeners.append(listener)
