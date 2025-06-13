
from especialidad import Especialidad
from excepciones import MedicoInvalidoException, MedicoYaExisteError, MedicoNoEncontradoError
from typing import Optional

class Medico:
    def __init__(self, nombre: str, matricula: str, especialidades: list[Especialidad] = None):
        if not nombre or not isinstance(nombre, str):
            raise MedicoInvalidoException("El nombre del médico es inválido.")
        if not matricula or not isinstance(matricula, str):
            raise MedicoInvalidoException("La matrícula del médico es inválida.")

        self.__nombre = nombre
        self.__matricula = matricula
        self.__especialidades = especialidades if especialidades else []

    def agregar_especialidad(self, especialidad: Especialidad):
        nombres_especialidades = [e.obtener_especialidad() for e in self.__especialidades]
        if especialidad.obtener_especialidad() in nombres_especialidades:
            raise MedicoYaExisteError("El médico ya tiene esta especialidad.")
        self.__especialidades.append(especialidad)

    def eliminar_especialidad(self, especialidad: Especialidad):
        nombres_especialidades = [e.obtener_especialidad() for e in self.__especialidades]
        if especialidad.obtener_especialidad() not in nombres_especialidades:
            raise MedicoNoEncontradoError("La especialidad no está asignada a este médico.")
        self.__especialidades = [e for e in self.__especialidades if e.obtener_especialidad() != especialidad.obtener_especialidad()]

    def obtener_matricula(self) -> str:
        return self.__matricula

    def obtener_especialidad_para_dia(self, dia: str) -> Optional[str]:
        dia = dia.lower()
        for especialidad in self.__especialidades:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None

    def __str__(self) -> str:
        especialidades_str = ", ".join(str(e) for e in self.__especialidades)
        return f"{self.__nombre}, {self.__matricula}, [{especialidades_str}]"
