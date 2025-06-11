import unittest
from paciente import Paciente
from excepciones import DatosPacienteInvalidosError, PacienteYaExisteError, PacienteNoEncontradoError

class TestPaciente(unittest.TestCase):

    def test_creacion_valida(self):
        paciente = Paciente("Zoe Camus", "46288610", "08/06/2005")
        self.assertEqual(paciente.obtener_dni(), "46288610")
        self.assertEqual(str(paciente), "Zoe Camus, 46288610, 08/06/2005")

    def test_nombre_vacio(self):
        with self.assertRaises(DatosPacienteInvalidosError):
            Paciente("", "46288610", "08/06/2005")

    def test_nombre_no_str(self):
        with self.assertRaises(DatosPacienteInvalidosError):
            Paciente(12345, "46288610", "08/06/2005")

    def test_dni_corto(self):
        with self.assertRaises(DatosPacienteInvalidosError):
            Paciente("Zoe Camus", "123456", "08/06/2005")

    def test_dni_largo(self):
        with self.assertRaises(DatosPacienteInvalidosError):
            Paciente("Zoe Camus", "123456789", "08/06/2005")

    def test_dni_no_numerico(self):
        with self.assertRaises(DatosPacienteInvalidosError):
            Paciente("Zoe Camus", "abc12345", "08/06/2005")

    def test_fecha_formato_invalido_guiones(self):
        with self.assertRaises(DatosPacienteInvalidosError):
            Paciente("Zoe Camus", "46288610", "2005-06-08")

    def test_fecha_formato_invalido_mes_dia_ano(self):
        with self.assertRaises(DatosPacienteInvalidosError):
            Paciente("Zoe Camus", "46288610", "06/08/05")

    def test_fecha_invalida_no_existente(self):
        with self.assertRaises(DatosPacienteInvalidosError):
            Paciente("Zoe Camus", "46288610", "31/02/2005")

    def test_agregar_paciente_ya_existe_error(self):
        pacientes = {}
        paciente = Paciente("Zoe Camus", "46288610", "08/06/2005")
        Paciente.agregar_paciente_a_coleccion(paciente, pacientes)  # agrego paciente
        with self.assertRaises(PacienteYaExisteError):
            Paciente.agregar_paciente_a_coleccion(paciente, pacientes)  # intento agregar otra vez

    def test_buscar_paciente_no_encontrado_error(self):
        pacientes = {}
        with self.assertRaises(PacienteNoEncontradoError):
            Paciente.buscar_paciente_por_dni("99999999", pacientes)

    def test_buscar_paciente_exitoso(self):
        pacientes = {}
        paciente = Paciente("Zoe Camus", "46288610", "08/06/2005")
        Paciente.agregar_paciente_a_coleccion(paciente, pacientes)
        encontrado = Paciente.buscar_paciente_por_dni("46288610", pacientes)
        self.assertEqual(encontrado, paciente)

if __name__ == "__main__":
    unittest.main()
