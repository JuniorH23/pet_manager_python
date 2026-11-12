from abc import ABC, abstractmethod

class AbstHospital(ABC):
    def __init__(self):
        # En Python, el guion bajo al inicio denota un atributo "privado" o protegido
        self._data = None 

    @abstractmethod
    def get_patient_type(self):
        pass

    @abstractmethod
    def surgery(self):
        pass

    def get_hospital_information(self):
        return f"La información es: {self.get_data()}"

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data