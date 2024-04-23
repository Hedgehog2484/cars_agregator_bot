from abc import ABC, abstractmethod


class IAiConnector(ABC):

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def convert_text(self, prompt: str, original_text: str) -> str:
        pass
