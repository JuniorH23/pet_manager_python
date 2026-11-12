from Interfaces.IAnimal import IAnimal
from Interfaces.lVertebrate import IVertebrate


class ClsPet(IAnimal, IVertebrate):

    def __init__(self, pet_id=None, code=None, name=None, born_year=0, color=None, health_status=None):
        self._pet_id = pet_id
        self._code = code
        self._name = name
        self._born_year = born_year
        self._color = color
        self._health_status = health_status
        self._veterinary = None  # Instancia de ClsVeterinary (asociación)

    # Comportamientos de la mascota
    def eat(self):
        print(f"La mascota {self._name} está comiendo.")

    def move(self):
        print(f"La mascota {self._name} está moviéndose.")

    def sound(self):
        print(f"La mascota {self._name} está relaizando el sonido.")

    # Implementación de los métodos de las interfaces (IAnimal e IVertebrate)
    def get_animal_type(self):
        return "Pet"

    def get_number_of_bones(self):
        return 0

    # Getters y Setters
    def get_pet_id(self):
        return self._pet_id

    def set_pet_id(self, pet_id):
        self._pet_id = pet_id

    def get_code(self):
        return self._code

    def set_code(self, code):
        self._code = code

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_born_year(self):
        return self._born_year

    def set_born_year(self, born_year):
        self._born_year = born_year

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def get_health_status(self):
        return self._health_status

    def set_health_status(self, health_status):
        self._health_status = health_status

    def get_veterinary(self):
        return self._veterinary

    def set_veterinary(self, veterinary):
        self._veterinary = veterinary