import unittest
from datetime import datetime
from paciente import Paciente
from medico import Medico
from receta import Receta
from excepciones import RecetaInvalidaException

class TestReceta(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Juan Perez", "12345678", "01/01/1980")
        self.medico = Medico("Dra. Ana Gomez", "M1234")

    def test_creacion_valida(self):
        fecha = datetime(2025, 6, 10)
        medicamentos = ["Paracetamol 500mg", "Ibuprofeno 200mg"]
        indicaciones = "Tomar después de las comidas"
        receta = Receta(self.paciente, self.medico, fecha, medicamentos, indicaciones)
        self.assertEqual(receta.paciente.obtener_dni(), "12345678")
        self.assertEqual(receta.medico.obtener_matricula(), "M1234")
        self.assertEqual(receta.fecha, fecha)
        self.assertListEqual(receta.medicamentos, medicamentos)
        self.assertEqual(receta.indicaciones, indicaciones)

    def test_creacion_sin_indicaciones(self):
        fecha = datetime(2025, 6, 10)
        medicamentos = ["Amoxicilina 500mg"]
        receta = Receta(self.paciente, self.medico, fecha, medicamentos)
        self.assertEqual(receta.indicaciones, "")

    def test_paciente_invalido(self):
        fecha = datetime(2025, 6, 10)
        medicamentos = ["Paracetamol"]
        with self.assertRaises(RecetaInvalidaException):
            Receta("no es paciente", self.medico, fecha, medicamentos)

    def test_medico_invalido(self):
        fecha = datetime(2025, 6, 10)
        medicamentos = ["Paracetamol"]
        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, "no es medico", fecha, medicamentos)

    def test_fecha_invalida(self):
        medicamentos = ["Paracetamol"]
        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, self.medico, "10/06/2025", medicamentos)

    def test_medicamentos_invalidos_tipo(self):
        fecha = datetime(2025, 6, 10)
        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, self.medico, fecha, "Paracetamol")

    def test_medicamentos_lista_vacia(self):
        fecha = datetime(2025, 6, 10)
        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, self.medico, fecha, [])

    def test_medicamentos_con_cadenas_vacias(self):
        fecha = datetime(2025, 6, 10)
        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, self.medico, fecha, ["Paracetamol", ""])

    def test_indicaciones_no_string(self):
        fecha = datetime(2025, 6, 10)
        medicamentos = ["Paracetamol"]
        with self.assertRaises(RecetaInvalidaException):
            Receta(self.paciente, self.medico, fecha, medicamentos, indicaciones=1234)

    def test_str_devuelve_informacion(self):
        fecha = datetime(2025, 6, 10)
        medicamentos = ["Paracetamol 500mg", "Ibuprofeno 200mg"]
        indicaciones = "Tomar con agua"
        receta = Receta(self.paciente, self.medico, fecha, medicamentos, indicaciones)
        salida = str(receta)
        self.assertIn("Juan Perez", salida)
        self.assertIn("Dra. Ana Gomez", salida)
        self.assertIn("10/06/2025", salida)
        self.assertIn("Paracetamol 500mg", salida)
        self.assertIn("Ibuprofeno 200mg", salida)
        self.assertIn("Tomar con agua", salida)

if __name__ == '__main__':
    unittest.main()
