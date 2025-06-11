import unittest
from datetime import datetime
from turno import Turno
from excepciones import TurnoOcupadoError, TurnoDuplicadoError, TurnoNoEncontradoError, TurnoError
from paciente import Paciente
from medico import Medico
from especialidad import Especialidad

class TestTurno(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Ana Pérez", "12345678", "01/01/1990")
        especialidad = Especialidad("Pediatría", ["lunes", "martes"])
        self.medico = Medico("Dr. Juan", "M1234", [especialidad])

        Turno._turnos.clear()

    def test_crear_turno_valido(self):
        fecha_hora = datetime(2025, 6, 10, 15, 0)
        turno = Turno(self.paciente, self.medico, fecha_hora)
        self.assertIn(turno, Turno.obtener_turnos())
        self.assertEqual(turno.paciente.obtener_dni(), "12345678")
        self.assertEqual(turno.medico.obtener_matricula(), "M1234")

    def test_turno_duplicado_paciente(self):
        fecha_hora = datetime(2025, 6, 10, 15, 0)
        Turno(self.paciente, self.medico, fecha_hora)
        with self.assertRaises(TurnoDuplicadoError):
            Turno(self.paciente, self.medico, fecha_hora)  

    def test_turno_ocupado_medico(self):
        paciente2 = Paciente("Pedro Gómez", "87654321", "02/02/1985")
        fecha_hora = datetime(2025, 6, 10, 15, 0)
        Turno(self.paciente, self.medico, fecha_hora)
        with self.assertRaises(TurnoOcupadoError):
            Turno(paciente2, self.medico, fecha_hora)  

    def test_buscar_turno_existente(self):
        fecha_hora = datetime(2025, 6, 10, 15, 0)
        turno = Turno(self.paciente, self.medico, fecha_hora)
        resultado = Turno.buscar_turno(self.paciente, fecha_hora)
        self.assertEqual(resultado, turno)

    def test_buscar_turno_no_existente(self):
        fecha_hora = datetime(2025, 6, 10, 15, 0)
        with self.assertRaises(TurnoNoEncontradoError):
            Turno.buscar_turno(self.paciente, fecha_hora)

    def test_eliminar_turno_existente(self):
        fecha_hora = datetime(2025, 6, 10, 15, 0)
        turno = Turno(self.paciente, self.medico, fecha_hora)
        Turno.eliminar_turno(self.paciente, fecha_hora)
        self.assertNotIn(turno, Turno.obtener_turnos())

    def test_eliminar_turno_no_existente(self):
        fecha_hora = datetime(2025, 6, 10, 15, 0)
        with self.assertRaises(TurnoNoEncontradoError):
            Turno.eliminar_turno(self.paciente, fecha_hora)

    def test_crear_turno_datos_invalidos(self):
        fecha_hora = datetime(2025, 6, 10, 15, 0)
        with self.assertRaises(TurnoError):
            Turno("no_paciente", self.medico, fecha_hora)
        with self.assertRaises(TurnoError):
            Turno(self.paciente, "no_medico", fecha_hora)
        with self.assertRaises(TurnoError):
            Turno(self.paciente, self.medico, "no_fecha")

if __name__ == "__main__":
    unittest.main()
