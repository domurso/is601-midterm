from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event, data):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event, data):
        for observer in self._observers:
            observer.update(event, data)
