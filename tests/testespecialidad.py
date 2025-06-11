import unittest
from especialidad import Especialidad
from excepciones import DatosEspecialidadInvalidosError

class TestEspecialidad(unittest.TestCase):
    def test_creacion_valida(self):
        esp = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])
        self.assertEqual(esp.obtener_especialidad(), "Pediatría")
        self.assertTrue(esp.verificar_dia("Lunes"))  
        self.assertFalse(esp.verificar_dia("domingo"))
        self.assertEqual(str(esp), "Pediatría (Días: lunes, miércoles, viernes)")

    def test_dias_invalidos(self):
        with self.assertRaises(DatosEspecialidadInvalidosError):
            Especialidad("Pediatría", ["Lunis", "Martis"])

    def test_dias_duplicados(self):
        with self.assertRaises(DatosEspecialidadInvalidosError):
            Especialidad("Cardiología", ["lunes", "lunes"])

    def test_sin_dias(self):
        with self.assertRaises(DatosEspecialidadInvalidosError):
            Especialidad("Dermatología", [])

    def test_especialidad_vacia(self):
        with self.assertRaises(DatosEspecialidadInvalidosError):
            Especialidad("", ["lunes", "martes"])

    def test_dias_finde_semana(self):
        with self.assertRaises(DatosEspecialidadInvalidosError):
            Especialidad("Pediatría", ["sábado", "domingo"])

    def test_dias_mixtos_validos_invalidos(self):
        with self.assertRaises(DatosEspecialidadInvalidosError):
            Especialidad("Clínica", ["lunes", "domingo"])

    def test_tipo_no_string(self):
        with self.assertRaises(DatosEspecialidadInvalidosError):
            Especialidad(123, ["lunes", "martes"])

    def test_dias_no_lista(self):
        with self.assertRaises(DatosEspecialidadInvalidosError):
            Especialidad("Oftalmología", "lunes")

if __name__ == '__main__':
    unittest.main()
