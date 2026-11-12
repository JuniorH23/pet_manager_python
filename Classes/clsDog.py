from Classes.clsPet import ClsPet


class ClsDog(ClsPet):

    # Unificación de los constructores de Java mediante parámetros por defecto
    def __init__(self, dog_id=None, breed=None, pedigree=False, pet_id=None, 
                 code=None, name=None, born_year=0, color=None, health_status=None):
        super().__init__(pet_id, code, name, born_year, color, health_status)
        self._dog_id = dog_id
        self._breed = breed
        self._pedigree = pedigree

    # Manejo de la sobrecarga del método WalkAround
    def walk_around(self, val=None):
        if val is None:
            print(f"El perro {self.get_name()} está caminando.")
        elif isinstance(val, bool):
            has_leash = "con correa" if val else "sin correa"
            print(f"El perro {self.get_name()} está caminando {has_leash}")
        elif isinstance(val, (int, float)):
            print(f"El perro {self.get_name()} está caminando {val} km")

    # Métodos sobreescritos (@Override)
    def sound(self):
        print(f"El perro {self.get_name()} hace Guuuuaaaauuu")

    def get_animal_type(self):
        return "Dog"

    def get_number_of_bones(self):
        return 320

    # Getters y Setters
    def get_breed(self):
        return self._breed

    def set_breed(self, breed):
        self._breed = breed

    def is_pedigree(self):
        return self._pedigree

    def set_pedigree(self, pedigree):
        self._pedigree = pedigree

    def get_dog_id(self):
        return self._dog_id

    def set_dog_id(self, dog_id):
        self._dog_id = dog_id