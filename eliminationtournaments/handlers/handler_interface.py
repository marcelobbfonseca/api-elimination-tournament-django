from abc import ABC, abstractmethod

class HandlerInterface(ABC):

    @abstractmethod
    def execute(self):
        pass