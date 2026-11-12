from Model.modelPet import ModelPet


class ModelCat(ModelPet):
    def __init__(self):
        super().__init__("Cat")

    def list_cat_by_health_status(self) -> list:
        return self.list_animal_by_health_status()
