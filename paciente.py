import re
from datetime import datetime
from excepciones import DatosPacienteInvalidosError, PacienteYaExisteError, PacienteNoEncontradoError

class Paciente:
    def __init__(self, nombre_apellido: str, dni: str, fecha_nacimiento: str):
        if not nombre_apellido or not isinstance(nombre_apellido, str):
            raise DatosPacienteInvalidosError("El nombre y apellido del paciente es inválido.")
        
        if not re.match(r'^\d{7,8}$', dni):
            raise DatosPacienteInvalidosError("El DNI debe tener 7 u 8 dígitos numéricos.")
        
        try:
            datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
        except ValueError:
            raise DatosPacienteInvalidosError("La fecha de nacimiento debe tener el formato dd/mm/aaaa.")
        
        self.__nombre_apellido = nombre_apellido
        self.dni = dni  
        self.__fecha_nacimiento = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.dni

    def __str__(self) -> str:
        return f"{self.__nombre_apellido}, {self.dni}, {self.__fecha_nacimiento}"

    @staticmethod
    def agregar_paciente_a_coleccion(paciente, coleccion):
        if paciente.dni in coleccion:
            raise PacienteYaExisteError(f"Paciente con DNI {paciente.dni} ya existe.")
        coleccion[paciente.dni] = paciente

    @staticmethod
    def buscar_paciente_por_dni(dni, coleccion):
        if dni not in coleccion:
            raise PacienteNoEncontradoError(f"Paciente con DNI {dni} no encontrado.")
        return coleccion[dni]
    def __eq__(self, other):
        if not isinstance(other, Paciente):
            return False
        return self.dni == other.dni

    def __hash__(self):
        return hash(self.dni)