# Python implementation for the bloc pattern
## Motivation
The project is motivated by [dart's bloc library](https://pub.dev/packages/bloc). Bloc design pattern helps to separate presentation from business logic.

## Main features
### Bloc <br>
A bloc relies on events to trigger states i.e a bloc receives events and convert the incoming events into outgoing states
### BlocObserver <br>
A bloc observer listens to state changes of a bloc and it is intended to influence the presentation layer
### State <br>
Contains information of how the presentation layer looks like
### Event <br>
Triggers the bloc which in turn provides new states
<br>
## Example 1 - Counter Bloc

### Bloc
```python
from bloc import Bloc
from enum import Enum


class Events(Enum):
    increment = 0
    decrement = 1


class CounterBloc(Bloc):

    def __init__(self) -> None:
        super().__init__(0)
        self.on(Events.increment, self.__increment)
        self.on(Events.decrement, self.__decrement)

    def __increment(self, emit):
        emit(self.current_state() + 1)

    def __decrement(self, emit):
        emit(self.current_state() - 1)

```

### Testing
```python
from bloc import bloc_test

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
```

### Adding Observers
```python
from bloc import BlocObserver

class MyObserver(BlocObserver):

    def on_change(self, old_state, new_state):
        print(f"MyObserver: old_state: {old_state} new_state: {new_state}")        


bloc = CounterBloc()
bloc.set_observer(MyObserver())
bloc.add(Events.increment)
bloc.add(Events.decrement)
```
#### output
```terminal
MyObserver: old_state: 0 new_state: 1
MyObserver: old_state: 1 new_state: 0
```