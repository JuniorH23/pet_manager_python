class ClsVeterinary(AbstHospital):

    def __init__(self, name=None, phone=None, address=None, doctor=None):
        super().__init__()
        self._name = name
        self._phone = phone
        self._address = address
        self._doctor = doctor

    def pet_care(self, pet):
        print(f"Atendiendo a la mascota {pet.get_name()}")
        return pet.get_health_status()

    # Métodos abstractos heredados de AbstHospital
    def get_patient_type(self):
        return "Animal"

    def surgery(self):
        return "Surgery animal data"

    # Getters y Setters
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_phone(self):
        return self._phone

    def set_phone(self, phone):
        self._phone = phone

    def get_address(self):
        return self._address

    def set_address(self, address):
        self._address = address

    def get_doctor(self):
        return self._doctor

    def set_doctor(self, doctor):
        self._doctor = doctor