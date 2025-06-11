
import unittest
from clinica import Clinica
from historia_clinica import HistoriaClinica
from paciente import Paciente
from excepciones import (
    ClinicaError,
    HistoriaClinicaDuplicadaError,
    HistoriaClinicaNoEncontradaError
)
class TestClinica(unittest.TestCase):
    def setUp(self):
        # Limpiar historias previas para evitar duplicados
        HistoriaClinica._historias.clear()
        self.clinica = Clinica("Clínica Central")
        self.paciente1 = Paciente("Juan Perez", "12345678", "01/01/1980")
        self.paciente2 = Paciente("Ana Gómez", "87654321", "15/05/1990")
        self.historia1 = HistoriaClinica(self.paciente1)
        self.historia2 = HistoriaClinica(self.paciente2)
    def test_agregar_historia_valida(self):
        self.clinica.agregar_historia_clinica(self.historia1)
        self.assertIn(self.historia1, self.clinica.historias_clinicas)
    def test_agregar_historia_duplicada(self):
        self.clinica.agregar_historia_clinica(self.historia1)
        with self.assertRaises(HistoriaClinicaDuplicadaError):
            self.clinica.agregar_historia_clinica(self.historia1)
    def test_buscar_historia_existente(self):
        self.clinica.agregar_historia_clinica(self.historia1)
        historia = self.clinica.buscar_historia_por_paciente(self.paciente1)
        self.assertEqual(historia, self.historia1)
    def test_buscar_historia_inexistente(self):
        with self.assertRaises(HistoriaClinicaNoEncontradaError):
            self.clinica.buscar_historia_por_paciente(self.paciente1)
    def test_eliminar_historia_valida(self):
        self.clinica.agregar_historia_clinica(self.historia1)
        self.clinica.eliminar_historia_clinica(self.paciente1)
        self.assertNotIn(self.historia1, self.clinica.historias_clinicas)
    def test_eliminar_historia_inexistente(self):
        with self.assertRaises(HistoriaClinicaNoEncontradaError):
            self.clinica.eliminar_historia_clinica(self.paciente2)
    def test_listar_historias(self):
        self.clinica.agregar_historia_clinica(self.historia1)
        self.clinica.agregar_historia_clinica(self.historia2)
        historias = self.clinica.listar_historias()
        self.assertIn(self.historia1, historias)
        self.assertIn(self.historia2, historias)
    def test_str_clinica(self):
        self.clinica.agregar_historia_clinica(self.historia1)
        texto = str(self.clinica)
        self.assertIn("Clínica Central", texto)
        self.assertIn("1 historias clínicas", texto)
if __name__ == "__main__":
    unittest.main()