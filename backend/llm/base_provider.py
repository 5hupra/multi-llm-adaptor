from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        message: list,
        temperature: float=0.7,
        max_tokens: int=500,
        stream: bool=false,
    ) -> dict:
        pass