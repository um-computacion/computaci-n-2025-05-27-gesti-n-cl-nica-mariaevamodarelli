from excepciones import (
    ClinicaError, HistoriaClinicaNoEncontradaError, HistoriaClinicaDuplicadaError,
    MedicoYaExisteError, MedicoNoEncontradoError, TurnoDuplicadoError, TurnoOcupadoError,
    PacienteNoEncontradoError, RecetaInvalidaException
)
from turno import Turno
from historia_clinica import HistoriaClinica
from receta import Receta
from datetime import datetime

class Clinica:
    def __init__(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClinicaError("El nombre de la clínica debe ser un string no vacío.")
        self.nombre = nombre
        self.historias_clinicas = []
        self.medicos = []
        self.turnos = []
        self.especialidades = []

    def agregar_historia_clinica(self, historia):
        if any(h.paciente == historia.paciente for h in self.historias_clinicas):
            raise HistoriaClinicaDuplicadaError("Ya existe una historia clínica para este paciente.")
        self.historias_clinicas.append(historia)

    def buscar_historia_por_paciente(self, paciente):
        for historia in self.historias_clinicas:
            if historia.paciente == paciente:
                return historia
        raise PacienteNoEncontradoError("No se encontró la historia clínica para el paciente.")

    def eliminar_historia_clinica(self, paciente):
        for historia in self.historias_clinicas:
            if historia.paciente == paciente:
                self.historias_clinicas.remove(historia)
                return
        raise HistoriaClinicaNoEncontradaError("No se encontró la historia clínica para el paciente.")

    def agregar_medico(self, medico):
        if any(m.obtener_matricula() == medico.obtener_matricula() for m in self.medicos):
            raise MedicoYaExisteError("Ya existe un médico con esa matrícula.")
        self.medicos.append(medico)

    def agregar_especialidad(self, especialidad):
        if especialidad not in self.especialidades:
            self.especialidades.append(especialidad)

    def agendar_turno(self, paciente, matricula_medico, fecha_hora):
        historia = self.buscar_historia_por_paciente(paciente)
        medico = self.buscar_medico_por_matricula(matricula_medico)

        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)
        especialidad = medico.obtener_especialidad_para_dia(dia_semana)

        if not especialidad:
            raise ClinicaError("El médico no atiende ninguna especialidad ese día.")

        for turno in self.turnos:
            if turno.medico == medico and turno.fecha_hora == fecha_hora:
                raise TurnoOcupadoError("El médico ya tiene un turno en ese horario.")
            if turno.paciente == paciente and turno.fecha_hora == fecha_hora:
                raise TurnoDuplicadoError("Este paciente ya tiene un turno en ese horario.")

        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.turnos.append(turno)
        historia.agregar_turno(turno)

    def emitir_receta(self, paciente, descripcion):
        historia = self.buscar_historia_por_paciente(paciente)
        medico = None

        if not self.medicos:
            raise RecetaInvalidaException("No hay médicos registrados para emitir receta.")

        # Solo para prueba, tomamos al primer médico
        medico = self.medicos[0]

        receta = Receta(paciente, medico, datetime.now(), [descripcion])
        historia.agregar_entrada(medico, "Receta emitida", [receta])

    def buscar_medico_por_matricula(self, matricula):
        for m in self.medicos:
            if m.obtener_matricula() == matricula:
                return m
        raise MedicoNoEncontradoError("No se encontró un médico con esa matrícula.")

    def listar_turnos(self):
        return self.turnos

    def listar_pacientes(self):
        return [h.paciente for h in self.historias_clinicas]

    def listar_medicos(self):
        return self.medicos

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]

    def __str__(self):
        return f"Clínica {self.nombre} con {len(self.historias_clinicas)} historias clínicas registradas."
