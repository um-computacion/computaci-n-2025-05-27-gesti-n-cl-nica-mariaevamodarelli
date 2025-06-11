from datetime import datetime
from paciente import Paciente
from medico import Medico
from receta import Receta
from turno import Turno
from excepciones import (
    HistoriaClinicaError,
    HistoriaClinicaNoEncontradaError,
    HistoriaClinicaDuplicadaError,
    HistoriaClinicaSinRecetasError,
)

class HistoriaClinica:
    _historias = []

    def __init__(self, paciente: Paciente):
        if not isinstance(paciente, Paciente):
            raise HistoriaClinicaError("Paciente inválido.")

        if any(hc.paciente.obtener_dni() == paciente.obtener_dni() for hc in HistoriaClinica._historias):
            raise HistoriaClinicaDuplicadaError("Ya existe una historia clínica para este paciente.")

        self.paciente = paciente
        self.entradas = []
        HistoriaClinica._historias.append(self)

    def agregar_entrada(self, medico: Medico, nota: str = "", recetas: list = None):
        if not isinstance(medico, Medico):
            raise HistoriaClinicaError("Médico inválido.")

        if recetas and not all(isinstance(r, Receta) for r in recetas):
            raise HistoriaClinicaError("Lista de recetas inválida.")

        entrada = {
            "fecha": datetime.now(),
            "medico": medico,
            "nota": nota,
            "recetas": recetas if recetas else [],
        }
        self.entradas.append(entrada)

    def agregar_turno(self, turno: Turno):
        self.entradas.append({
            "fecha": turno.obtener_fecha_hora(),
            "medico": turno.obtener_medico(),
            "nota": f"Turno para {turno.obtener_especialidad()}",
            "recetas": []
        })

    def obtener_recetas(self):
        todas = []
        for entrada in self.entradas:
            todas.extend(entrada["recetas"])

        if not todas:
            raise HistoriaClinicaSinRecetasError("No hay recetas registradas.")

        return todas

    def obtener_notas(self):
        return [e["nota"] for e in self.entradas if e["nota"]]

    @classmethod
    def buscar_por_paciente(cls, paciente: Paciente):
        for hc in cls._historias:
            if hc.paciente.obtener_dni() == paciente.obtener_dni():
                return hc
        raise HistoriaClinicaNoEncontradaError("No se encontró la historia clínica del paciente.")

    @classmethod
    def eliminar_historia(cls, paciente: Paciente):
        historia = None
        for hc in cls._historias:
            if hc.paciente.obtener_dni() == paciente.obtener_dni():
                historia = hc
                break
        if historia:
            cls._historias.remove(historia)
        else:
            raise HistoriaClinicaNoEncontradaError("No se puede eliminar: historia no encontrada.")

    def __str__(self):
        resumen = f"Historia clínica de {self.paciente}:\n"
        for entrada in self.entradas:
            fecha = entrada["fecha"].strftime("%d/%m/%Y %H:%M")
            resumen += f"- {fecha} | Médico: {entrada['medico']} | Nota: {entrada['nota']}\n"
        return resumen.strip()
