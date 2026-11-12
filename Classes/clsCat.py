from Classes.clsPet import ClsPet


class ClsCat(ClsPet):
    
    # Se unifican los dos constructores de Java usando valores por defecto (None o 0)
    def __init__(self, cat_id=None, breed=None, pet_id=None, code=None, name=None, 
                 born_year=0, color=None, health_status=None):
        # Llamada al constructor de la clase padre (super)
        super().__init__(pet_id, code, name, born_year, color, health_status)
        
        # Atributos "privados" indicados con el guion bajo
        self._cat_id = cat_id
        self._breed = breed

    # Getters y Setters
    def get_cat_id(self):
        return self._cat_id

    def set_cat_id(self, cat_id):
        self._cat_id = cat_id

    def get_breed(self):
        return self._breed

    def set_breed(self, breed):
        self._breed = breed

    # Métodos de la clase
    def self_cleaning(self):
        # Se asume que la clase padre clsPet tiene un método get_name()
        print(f"El gato {self.get_name()} se está limpiando.")

    # Equivalente a @Override (en Python se sobreescribe simplemente usando el mismo nombre)
    def sound(self):
        print(f"El gato {self.get_name()} hace miaaauuu")

    def get_number_of_bones(self):
        return 230

    def get_animal_type(self):
        return "Cat"