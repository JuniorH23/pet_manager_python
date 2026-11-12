class ClsReportByHealthStatus:
    def __init__(self, health_status=None, amount_of_pets_by_health_status=0):
        # Atributos encapsulados con guion bajo por convención
        self._health_status = health_status
        self._amount_of_pets_by_health_status = amount_of_pets_by_health_status

    # Getters y Setters para 'health_status'
    def get_health_status(self):
        return self._health_status

    def set_health_status(self, health_status):
        self._health_status = health_status

    # Getters y Setters para 'amount_of_pets_by_health_status'
    def get_amount_of_pets_by_health_status(self):
        return self._amount_of_pets_by_health_status

    def set_amount_of_pets_by_health_status(self, amount_of_pets_by_health_status):
        self._amount_of_pets_by_health_status = amount_of_pets_by_health_status