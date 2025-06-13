from excepciones import DatosEspecialidadInvalidosError
import unicodedata

class Especialidad:
    DIAS_VALIDOS = ["lunes", "martes", "miércoles", "jueves", "viernes"]

    def __init__(self, tipo: str, dias: list[str]):
        if not tipo or not isinstance(tipo, str):
            raise DatosEspecialidadInvalidosError("El nombre de la especialidad es inválido.")

        if not isinstance(dias, list) or len(dias) == 0:
            raise DatosEspecialidadInvalidosError("La lista de días es inválida o vacía.")

        # Función para quitar tildes
        def quitar_tildes(s):
            return ''.join(
                c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn'
            )

        # Normalizamos y quitamos tildes de los días ingresados
        dias_normalizados = [quitar_tildes(d.lower()) for d in dias]

        # También normalizamos DIAS_VALIDOS sin tildes para comparar
        dias_validos_sin_tilde = [quitar_tildes(d) for d in self.DIAS_VALIDOS]

        if not all(d in dias_validos_sin_tilde for d in dias_normalizados):
            raise DatosEspecialidadInvalidosError("Solo se puede atender de lunes a viernes.")

        if len(set(dias_normalizados)) != len(dias_normalizados):
            raise DatosEspecialidadInvalidosError("La lista de días contiene duplicados.")

        # Guardamos los días con tilde originales pero en minúscula (reconstruidos)
        # para que se muestre bien en __str__
        self.__tipo = tipo
        # Para mostrar, los buscamos en DIAS_VALIDOS por el índice del sin tilde
        self.__dias = [self.DIAS_VALIDOS[dias_validos_sin_tilde.index(d)] for d in dias_normalizados]

    def obtener_especialidad(self) -> str:
        return self.__tipo

    def verificar_dia(self, dia: str) -> bool:
        return dia.lower() in [d.lower() for d in self.__dias]

    def __str__(self) -> str:
        dias_str = ", ".join(self.__dias)
        return f"{self.__tipo} (Días: {dias_str})"
