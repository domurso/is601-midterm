from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event, data):  # pragma: no cover
        pass  # pragma: no cover

class Subject(ABC):
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):  # pragma: no cover
        if observer in self._observers:  # pragma: no cover
            self._observers.remove(observer)  # pragma: no cover

    def notify_observers(self, event, data):
        for observer in self._observers:
            observer.update(event, data)
