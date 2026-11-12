from abc import ABC, abstractmethod


class IAnimal(ABC):

    @abstractmethod
    def get_animal_type(self) -> str:
        pass