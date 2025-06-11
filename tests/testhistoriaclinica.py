import unittest
from datetime import datetime
from paciente import Paciente
from medico import Medico
from receta import Receta
from historia_clinica import HistoriaClinica
from excepciones import (
    HistoriaClinicaError,
    HistoriaClinicaNoEncontradaError,
    HistoriaClinicaDuplicadaError,
    HistoriaClinicaSinRecetasError,
)

class TestHistoriaClinica(unittest.TestCase):
    def setUp(self):
        # Crear paciente y médico válidos
        self.paciente = Paciente("Juan Perez", "12345678", "01/01/1990")
        self.medico = Medico("Dr. Ana", "MAT12345")
        self.historia = HistoriaClinica(self.paciente)

    def tearDown(self):
        # Limpiar las historias para evitar duplicados en tests
        HistoriaClinica._historias.clear()

    def test_crear_historia_valida(self):
        self.assertEqual(self.historia.paciente.obtener_dni(), self.paciente.obtener_dni())

    def test_crear_historia_duplicada(self):
        with self.assertRaises(HistoriaClinicaDuplicadaError):
            HistoriaClinica(self.paciente)  # Ya existe la historia creada en setUp

    def test_agregar_entrada_valida(self):
        receta = Receta(self.paciente, self.medico, datetime.now(), ["Paracetamol"], "Tomar 2 veces al día")
        self.historia.agregar_entrada(self.medico, "Paciente con fiebre", [receta])
        self.assertEqual(len(self.historia.entradas), 1)
        self.assertEqual(self.historia.entradas[0]["nota"], "Paciente con fiebre")
        self.assertEqual(len(self.historia.entradas[0]["recetas"]), 1)

    def test_agregar_entrada_medico_invalido(self):
        with self.assertRaises(HistoriaClinicaError):
            self.historia.agregar_entrada("no_es_medico", "Nota inválida")

    def test_obtener_recetas_no_hay(self):
        with self.assertRaises(HistoriaClinicaSinRecetasError):
            self.historia.obtener_recetas()

    def test_obtener_recetas_ok(self):
        receta = Receta(self.paciente, self.medico, datetime.now(), ["Ibuprofeno"])
        self.historia.agregar_entrada(self.medico, "Nota", [receta])
        recetas = self.historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)
        self.assertIsInstance(recetas[0], Receta)

    def test_buscar_por_paciente_existente(self):
        encontrada = HistoriaClinica.buscar_por_paciente(self.paciente)
        self.assertEqual(encontrada, self.historia)

    def test_buscar_por_paciente_no_existente(self):
        otro_paciente = Paciente("Maria Lopez", "87654321", "02/02/1985")
        with self.assertRaises(HistoriaClinicaNoEncontradaError):
            HistoriaClinica.buscar_por_paciente(otro_paciente)

    def test_eliminar_historia_existente(self):
        HistoriaClinica.eliminar_historia(self.paciente)
        with self.assertRaises(HistoriaClinicaNoEncontradaError):
            HistoriaClinica.buscar_por_paciente(self.paciente)

    def test_eliminar_historia_no_existente(self):
        otro_paciente = Paciente("Maria Lopez", "87654321", "02/02/1985")
        with self.assertRaises(HistoriaClinicaNoEncontradaError):
            HistoriaClinica.eliminar_historia(otro_paciente)

    def test_str_historia(self):
        self.historia.agregar_entrada(self.medico, "Consulta general")
        salida = str(self.historia)
        self.assertIn("Juan Perez", salida)
        self.assertIn("Consulta general", salida)

if __name__ == "__main__":
    unittest.main()
