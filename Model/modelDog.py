from Model.modelPet import ModelPet


class ModelDog(ModelPet):
    def __init__(self):
        super().__init__("Dog")

    def list_dog_by_health_status(self) -> list:
        return self.list_animal_by_health_status()
