class ctlPet:
    def __init__(self, model_dog, model_cat):
        self.model_dog = model_dog
        self.model_cat = model_cat

    def create_pet(self, pet) -> bool:
        animal_type = pet.get_animal_type()
        if animal_type == "Dog":
            return self.model_dog.create_pet(pet)
        if animal_type == "Cat":
            return self.model_cat.create_pet(pet)
        return False

    def search_pet(self, code: str, animal_type: str):
        if animal_type == "Cat":
            return self.model_cat.search_pet(code)
        if animal_type == "Dog":
            return self.model_dog.search_pet(code)
        return None

    def edit_pet(self, pet) -> bool:
        animal_type = pet.get_animal_type()
        if animal_type == "Cat":
            return self.model_cat.edit_pet(pet)
        if animal_type == "Dog":
            return self.model_dog.edit_pet(pet)
        return False

    def delete_pet(self, pet) -> bool:
        animal_type = pet.get_animal_type()
        if animal_type == "Cat":
            return self.model_cat.delete_pet(pet)
        if animal_type == "Dog":
            return self.model_dog.delete_pet(pet)
        return False

    def list_pet(self, animal_type: str) -> list:
        if animal_type == "Dog":
            return self.model_dog.list_pet()
        if animal_type == "Cat":
            return self.model_cat.list_pet()
        return []

    def list_pet_by_health_status(self) -> list:
        return self.model_cat.list_pet_by_health_status()

    def list_dog_by_health_status(self) -> list:
        return self.model_dog.list_dog_by_health_status()

    def list_cat_by_health_status(self) -> list:
        return self.model_cat.list_cat_by_health_status()
