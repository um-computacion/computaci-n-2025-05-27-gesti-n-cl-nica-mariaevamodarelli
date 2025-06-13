
from datetime import datetime
from clinica import Clinica
from paciente import Paciente
from medico import Medico
from especialidad import Especialidad
from historia_clinica import HistoriaClinica
from excepciones import *

class CLI:
    def __init__(self):
        self.clinica = Clinica("Clínica Central")

    def ejecutar(self):
        print("Bienvenido a la gestión de la clínica.\n")
        while True:
            print("\n--- Menú Clínica ---")
            print("1) Agregar paciente")
            print("2) Agregar médico")
            print("3) Agendar turno")
            print("4) Agregar especialidad")
            print("5) Emitir receta")
            print("6) Ver historia clínica")
            print("7) Ver todos los turnos")
            print("8) Ver todos los pacientes")
            print("9) Ver todos los médicos")
            print("0) Salir")
            opcion = input("Ingrese una opción: ")
            try:
                if opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.agregar_especialidad()
                elif opcion == "5":
                    self.emitir_receta()
                elif opcion == "6":
                    self.ver_historia_clinica()
                elif opcion == "7":
                    self.ver_todos_los_turnos()
                elif opcion == "8":
                    self.ver_todos_los_pacientes()
                elif opcion == "9":
                    self.ver_todos_los_medicos()
                elif opcion == "0":
                    print("Gracias por usar el sistema.")
                    break
                else:
                    print("Opción no válida.")
            except ClinicaError as e:
                print(f"Error de clínica: {e}")
            except DatosPacienteInvalidosError as e:
                print(f"Error en datos del paciente: {e}")
            except DatosEspecialidadInvalidosError as e:
                print(f"Error en datos de especialidad: {e}")
            except MedicoInvalidoException as e:
                print(f"Error en datos del médico: {e}")
            except RecetaInvalidaException as e:
                print(f"Error en receta: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

    def agregar_paciente(self):
        while True:
            try:
                nombre_apellido = input("Nombre y apellido del paciente (o 'cancelar' para volver): ").strip()
                if nombre_apellido.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                dni = input("DNI del paciente (o 'cancelar' para volver): ").strip()
                if dni.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                fecha_nac = input("Fecha de nacimiento (DD/MM/AAAA) (o 'cancelar' para volver): ").strip()
                if fecha_nac.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                paciente = Paciente(nombre_apellido, dni, fecha_nac)
                historia = HistoriaClinica(paciente)
                self.clinica.agregar_historia_clinica(historia)
                print("Paciente y su historia clínica agregados con éxito.")
                break
            except DatosPacienteInvalidosError as e:
                print(f"Error: {e}. Intente nuevamente o escriba 'cancelar' para volver.")

    def agregar_medico(self):
        while True:
            try:
                nombre_apellido = input("Nombre y apellido del médico (o 'cancelar' para volver): ").strip()
                if nombre_apellido.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                matricula = input("Matrícula del médico (o 'cancelar' para volver): ").strip()
                if matricula.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                medico = Medico(nombre_apellido, matricula)
                self.clinica.agregar_medico(medico)
                print("Médico agregado con éxito.")
                break
            except MedicoInvalidoException as e:
                print(f"Error: {e}. Intente nuevamente o escriba 'cancelar' para volver.")
            except MedicoYaExisteError as e:
                print(f"Error: {e}. Intente nuevamente o escriba 'cancelar' para volver.")

    def agendar_turno(self):
        while True:
            try:
                dni = input("DNI del paciente (o 'cancelar' para volver): ").strip()
                if dni.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                medico_matricula = input("Matrícula del médico (o 'cancelar' para volver): ").strip()
                if medico_matricula.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                fecha_turno = input("Fecha y hora del turno (DD/MM/AAAA HH:MM) (o 'cancelar' para volver): ").strip()
                if fecha_turno.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                try:
                    fecha_dt = datetime.strptime(fecha_turno, "%d/%m/%Y %H:%M")
                except ValueError:
                    print("Formato de fecha y hora inválido. Use DD/MM/AAAA HH:MM.")
                    continue
                self.clinica.agendar_turno_por_dni(dni, medico_matricula, fecha_dt)
                print("Turno agendado con éxito.")
                break
            except TurnoOcupadoError as e:
                print(f"Error: {e}. Intente otra fecha/hora.")
            except TurnoDuplicadoError as e:
                print(f"Error: {e}. Intente otra fecha/hora.")
            except PacienteNoEncontradoError as e:
                print(f"Error: {e}. Verifique el paciente.")
            except MedicoNoEncontradoError as e:
                print(f"Error: {e}. Verifique el médico.")
            except Exception as e:
                print(f"Error: {e}. Intente nuevamente.")

    def agregar_especialidad(self):
        while True:
            try:
                nombre = input("Nombre de la especialidad (o 'cancelar' para volver): ").strip()
                if nombre.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                dias_input = input("Día(s) de atención (ej: lunes, martes, miércoles) (o 'cancelar' para volver): ").strip()
                if dias_input.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                dias = [d.strip() for d in dias_input.split(",") if d.strip()]
                matricula = input("Matrícula del médico que la tendrá (o 'cancelar' para volver): ").strip()
                if matricula.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                especialidad = Especialidad(nombre, dias)
                medico = self.clinica.buscar_medico_por_matricula(matricula)
                medico.agregar_especialidad(especialidad)
                print("Especialidad agregada al médico con éxito.")
                break
            except MedicoNoEncontradoError as e:
                print(f"Error: {e}. Intente nuevamente o escriba 'cancelar' para volver.")
            except DatosEspecialidadInvalidosError as e:
                print(f"Error: {e}. Intente nuevamente o escriba 'cancelar' para volver.")
            except MedicoYaExisteError as e:
                print(f"Error: {e}. El médico ya tiene esa especialidad. Intente nuevamente o escriba 'cancelar' para volver.")
            except Exception as e:
                print(f"Error inesperado: {e}")

    def emitir_receta(self):
        while True:
            try:
                dni = input("DNI del paciente (o 'cancelar' para volver): ").strip()
                if dni.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                descripcion = input("Descripción de la receta (o 'cancelar' para volver): ").strip()
                if descripcion.lower() == "cancelar":
                    print("Operación cancelada.")
                    return
                self.clinica.emitir_receta_por_dni(dni, descripcion)
                print("Receta emitida con éxito.")
                break
            except RecetaInvalidaException as e:
                print(f"Error: {e}. Intente nuevamente o escriba 'cancelar' para volver.")
            except PacienteNoEncontradoError as e:
                print(f"Error: {e}. Verifique el paciente.")
            except Exception as e:
                print(f"Error: {e}. Intente nuevamente.")

    def ver_historia_clinica(self):
        dni = input("DNI del paciente: ").strip()
        try:
            historia = self.clinica.buscar_historia_por_dni(dni)
            print(historia)
        except HistoriaClinicaNoEncontradaError as e:
            print(f"Error: {e}")

    def ver_todos_los_turnos(self):
        turnos = self.clinica.listar_turnos()
        if not turnos:
            print("No hay turnos agendados.")
        else:
            for turno in turnos:
                print(turno)

    def ver_todos_los_pacientes(self):
        pacientes = self.clinica.listar_pacientes()
        if not pacientes:
            print("No hay pacientes registrados.")
        else:
            for paciente in pacientes:
                print(paciente)

    def ver_todos_los_medicos(self):
        medicos = self.clinica.listar_medicos()
        if not medicos:
            print("No hay médicos registrados.")
        else:
            for medico in medicos:
                print(medico)