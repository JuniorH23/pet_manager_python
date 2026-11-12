from abc import ABC, abstractmethod


class IVertebrate(ABC):

    @abstractmethod
    def get_number_of_bones(self) -> int:
        pass