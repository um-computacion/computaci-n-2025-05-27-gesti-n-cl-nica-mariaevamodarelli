
import unittest
from medico import Medico
from especialidad import Especialidad
from excepciones import MedicoInvalidoException, MedicoYaExisteError, MedicoNoEncontradoError

class TestMedico(unittest.TestCase):

    def setUp(self):
        self.especialidad1 = Especialidad("Cardiología", ["lunes", "miércoles"])
        self.especialidad2 = Especialidad("Dermatología", ["martes", "jueves"])

    def test_creacion_valida(self):
        medico = Medico("Dr. Juan Pérez", "MAT1234", [self.especialidad1])
        self.assertEqual(medico.obtener_matricula(), "MAT1234")
        self.assertIn(self.especialidad1, medico._Medico__especialidades)

    def test_nombre_invalido(self):
        with self.assertRaises(MedicoInvalidoException):
            Medico("", "MAT1234")

    def test_matricula_invalida(self):
        with self.assertRaises(MedicoInvalidoException):
            Medico("Dr. Juan Pérez", "")

    def test_agregar_especialidad_valida(self):
        medico = Medico("Dr. Juan Pérez", "MAT1234")
        medico.agregar_especialidad(self.especialidad1)
        self.assertIn(self.especialidad1, medico._Medico__especialidades)

    def test_agregar_especialidad_duplicada(self):
        medico = Medico("Dr. Juan Pérez", "MAT1234", [self.especialidad1])
        with self.assertRaises(MedicoYaExisteError):
            medico.agregar_especialidad(self.especialidad1)

    def test_eliminar_especialidad_valida(self):
        medico = Medico("Dr. Juan Pérez", "MAT1234", [self.especialidad1, self.especialidad2])
        medico.eliminar_especialidad(self.especialidad1)
        self.assertNotIn(self.especialidad1, medico._Medico__especialidades)
        self.assertIn(self.especialidad2, medico._Medico__especialidades)

    def test_eliminar_especialidad_no_existente(self):
        medico = Medico("Dr. Juan Pérez", "MAT1234", [self.especialidad2])
        with self.assertRaises(MedicoNoEncontradoError):
            medico.eliminar_especialidad(self.especialidad1)

    def test_obtener_especialidad_para_dia(self):
        medico = Medico("Dr. Juan Pérez", "MAT1234", [self.especialidad1, self.especialidad2])
        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Cardiología")
        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Dermatología")
        self.assertIsNone(medico.obtener_especialidad_para_dia("domingo"))

if __name__ == "__main__":
    unittest.main()



