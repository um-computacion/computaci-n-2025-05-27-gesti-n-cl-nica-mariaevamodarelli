from datetime import datetime
from paciente import Paciente
from medico import Medico
from excepciones import RecetaInvalidaException

class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, fecha: datetime, medicamentos: list[str], indicaciones: str = ""):
        if not isinstance(paciente, Paciente):
            raise RecetaInvalidaException("Paciente inválido.")
        if not isinstance(medico, Medico):
            raise RecetaInvalidaException("Médico inválido.")
        if not isinstance(fecha, datetime):
            raise RecetaInvalidaException("Fecha inválida.")
        if not isinstance(medicamentos, list) or len(medicamentos) == 0 or not all(isinstance(med, str) and med.strip() for med in medicamentos):
            raise RecetaInvalidaException("Lista de medicamentos inválida.")
        if not isinstance(indicaciones, str):
            raise RecetaInvalidaException("Indicaciones inválidas.")

        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha
        self.medicamentos = medicamentos
        self.indicaciones = indicaciones

    def __str__(self):
        meds = ", ".join(self.medicamentos)
        return f"Receta para {self.paciente} por {self.medico} el {self.fecha.strftime('%d/%m/%Y')}:\nMedicamentos: {meds}\nIndicaciones: {self.indicaciones}"
