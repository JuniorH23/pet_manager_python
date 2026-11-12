class ClsDoctor:
    def __init__(self, name, licence):
        # En Python, usamos self para referirnos a la instancia actual (equivalente a 'this')
        # El guion bajo indica por convención que son atributos "privados"
        self._name = name
        self._licence = licence

    # Getter y Setter para 'name'
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    # Getter y Setter para 'licence'
    def get_licence(self):
        return self._licence

    def set_licence(self, licence):
        self._licence = licence