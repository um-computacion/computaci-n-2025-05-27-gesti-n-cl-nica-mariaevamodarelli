from datetime import datetime
from paciente import Paciente
from medico import Medico
from excepciones import TurnoOcupadoError, TurnoDuplicadoError, TurnoNoEncontradoError, TurnoError

class Turno:
    _turnos = []

    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str):
        if not isinstance(paciente, Paciente):
            raise TurnoError("Paciente inválido.")
        if not isinstance(medico, Medico):
            raise TurnoError("Médico inválido.")
        if not isinstance(fecha_hora, datetime):
            raise TurnoError("Fecha y hora inválidas.")
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise TurnoError("Especialidad inválida.")

        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.especialidad = especialidad.strip()

        for turno in Turno._turnos:
            if (turno.paciente.obtener_dni() == self.paciente.obtener_dni() and
                turno.fecha_hora == self.fecha_hora):
                raise TurnoDuplicadoError("El paciente ya tiene un turno para esta fecha y hora.")

        for turno in Turno._turnos:
            if (turno.medico.obtener_matricula() == self.medico.obtener_matricula() and
                turno.fecha_hora == self.fecha_hora):
                raise TurnoOcupadoError("El médico ya tiene un turno en esta fecha y hora.")

        Turno._turnos.append(self)

    @classmethod
    def obtener_turnos(cls):
        return cls._turnos.copy()

    @classmethod
    def buscar_turno(cls, paciente: Paciente, fecha_hora: datetime):
        for turno in cls._turnos:
            if (turno.paciente.obtener_dni() == paciente.obtener_dni() and
                turno.fecha_hora == fecha_hora):
                return turno
        raise TurnoNoEncontradoError("No se encontró el turno solicitado.")

    @classmethod
    def eliminar_turno(cls, paciente: Paciente, fecha_hora: datetime):
        turno_a_eliminar = None
        for turno in cls._turnos:
            if (turno.paciente.obtener_dni() == paciente.obtener_dni() and
                turno.fecha_hora == fecha_hora):
                turno_a_eliminar = turno
                break
        if turno_a_eliminar:
            cls._turnos.remove(turno_a_eliminar)
        else:
            raise TurnoNoEncontradoError("No se encontró el turno para eliminar.")

    def obtener_medico(self) -> Medico:
        return self.medico

    def obtener_fecha_hora(self) -> datetime:
        return self.fecha_hora

    def obtener_especialidad(self) -> str:
        return self.especialidad

    def __str__(self):
        fecha_str = self.fecha_hora.strftime("%d/%m/%Y %H:%M")
        return f"Turno: {self.paciente} - {self.medico} - {fecha_str} - Especialidad: {self.especialidad}"
