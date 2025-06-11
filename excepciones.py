class DatosPacienteInvalidosError(Exception):
    pass

class DatosEspecialidadInvalidosError(Exception):
    pass

class MedicoInvalidoException(Exception):
    pass

class TurnoOcupadoError(Exception):
    pass    

class TurnoDuplicadoError(Exception):   
    pass

class TurnoNoEncontradoError(Exception):
    pass

class TurnoError(Exception):
    pass

class HistoriaClinicaError(Exception):
    pass

class HistoriaClinicaNoEncontradaError(Exception):
    pass

class HistoriaClinicaDuplicadaError(Exception):
    pass

class HistoriaClinicaSinRecetasError(Exception):
    pass

class RecetaInvalidaException(Exception):
    pass

class ClinicaError(Exception):
    pass

class PacienteYaExisteError(Exception):
    pass

class MedicoYaExisteError(Exception):
    pass

class PacienteNoEncontradoError(Exception):
    pass

class MedicoNoEncontradoError(Exception):
    pass
