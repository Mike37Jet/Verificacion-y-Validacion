from enum import Enum

from behave import *

use_step_matcher("re")


class Estudiante:
    def __init__(self, nombre, apellido, edad, cedula, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.cedula = cedula
        self.correo = correo
        self.carrera = None

    def registrar_asignatura(self, asignatura):
        if not hasattr(self, 'asignaturas'):
            self.asignaturas = []
        self.asignaturas.append(asignatura)

    def llenar_encuesta_del_semestre(self, semestre, asignaturas_con_objetivos=None):
        if not hasattr(self, 'historiales'):
            self.historiales = {}

        self.historiales[semestre] = {
            'asignaturas': [
                {
                    'nombre': asignatura.nombre,
                    'objetivos': [
                        {'objetivo': obj, 'valor': porcentaje}
                        for obj, porcentaje in objetivos_con_porcentaje
                    ]
                }
                for asignatura, objetivos_con_porcentaje in asignaturas_con_objetivos.items()
            ]
        }
        return self.historiales[semestre]

    def registrar_semestre(self, historial=None):
        if not hasattr(self, 'historiales'):
            self.historiales = {}

        # Si se proporciona un historial completo
        if isinstance(historial, dict) and 'asignaturas' in historial:
            # Extraer el semestre del historial actual o generar uno nuevo
            semestre = next(iter(self.historiales.keys()), None)
            if semestre is None:
                from datetime import datetime
                año = datetime.now().year
                periodo = "A" if datetime.now().month <= 6 else "B"
                semestre = f"{año}-{periodo}"

            # Guardar o actualizar el historial para este semestre
            self.historiales[semestre] = historial
            return semestre

        # Comportamiento anterior como fallback (si se pasa un semestre en vez de historial)
        semestre = historial  # Renombrado para claridad
        if semestre is None:
            from datetime import datetime
            año = datetime.now().year
            periodo = "A" if datetime.now().month <= 6 else "B"
            semestre = f"{año}-{periodo}"

        # Verificar si el semestre ya existe en los historiales
        if semestre not in self.historiales:
            self.historiales[semestre] = {}

        return semestre

    def obtener_progreso(self):
        if not hasattr(self, 'historiales'):
            return None

        # Inicializar progreso con todos los objetivos de la carrera con valor 0
        progreso = {objetivo: 0 for objetivo in self.carrera.objetivos} if self.carrera and hasattr(self.carrera,
                                                                                                    'objetivos') else {}

        # Actualizar los valores de progreso para los objetivos encontrados en los historiales
        for semestre, historial in self.historiales.items():
            for asignatura in historial['asignaturas']:
                for objetivo in asignatura['objetivos']:
                    if objetivo['objetivo'] not in progreso:
                        progreso[objetivo['objetivo']] = 0
                    progreso[objetivo['objetivo']] += objetivo['valor']

        # Convertir a porcentaje
        total_objetivos = len(self.asignaturas[0].objetivos) * len(self.historiales)
        for key in progreso:
            progreso[key] = min(100, (progreso[key] / total_objetivos) * 100)

        return progreso


class Asignatura:
    def __init__(self, nombre, objetivos):
        self.nombre = nombre
        self.objetivos = objetivos


class Carrera:
    def __init__(self, nombre, numero_de_objetivos, asignaturas):
        self.nombre = nombre
        self.numero_de_objetivos = numero_de_objetivos
        self.asignaturas = asignaturas
        self.umbral_aceptacion = 0
        self.objetivos = None
        self.estudiantes_matriculados = []  # Nueva lista para almacenar estudiantes

    # En la clase Carrera
    def validar_objetivos(self, num_objetivos, objetivos_disponibles):
        if num_objetivos > len(objetivos_disponibles):
            raise ValueError(
                f"Error: El número de objetivos solicitado ({num_objetivos}) excede los objetivos disponibles ({len(objetivos_disponibles)})")
        if num_objetivos < len(objetivos_disponibles):
            raise ValueError("Error: El número de objetivos debe ser mayor que los definidos en la carrera")

    def matricular_estudiante(self, estudiante):
        estudiante.carrera = self
        self.estudiantes_matriculados.append(estudiante)  # Añadir estudiante a la lista

    def establecer_umbral(self, umbral):
        self.umbral_aceptacion = umbral

    def verificar_progreso_estudiante(self, estudiante):
        if not hasattr(estudiante, 'historiales'):
            return False

        if self.umbral_aceptacion < 0:
            return False

        for semestre, historial in estudiante.historiales.items():
            for asignatura in historial['asignaturas']:
                for objetivo in asignatura['objetivos']:
                    if objetivo['valor'] < self.umbral_aceptacion:
                        return False
        return True

    def calcular_media_progreso(self):
        if not hasattr(self, 'asignaturas') or not self.asignaturas:
            return {}

        # Inicializar diccionario para acumular valores por objetivo
        suma_progreso = {}
        contador_estudiantes = 0

        # Usar la lista de estudiantes matriculados
        for estudiante in self.estudiantes_matriculados:
            contador_estudiantes += 1
            progreso_estudiante = estudiante.obtener_progreso()

            if progreso_estudiante:
                for objetivo, valor in progreso_estudiante.items():
                    if objetivo not in suma_progreso:
                        suma_progreso[objetivo] = 0
                    suma_progreso[objetivo] += valor

        # Calcular la media dividiendo la suma por el número de estudiantes
        media_progreso = {}
        if contador_estudiantes > 0:
            for objetivo, suma in suma_progreso.items():
                media_progreso[objetivo] = float(suma / contador_estudiantes)
        else:
            # Si no hay estudiantes, lanzar un error
            raise ValueError("No hay estudiantes matriculados para calcular la media de progreso")

        return media_progreso

    def mostrar_mensaje_felicitacion(self, estudiante):
        if not hasattr(estudiante, 'historiales') or not estudiante.historiales:
            return "No hay historial de progreso para mostrar."

        mensaje = f"¡Felicidades {estudiante.nombre}! Has superado satisfactoriamente todos los objetivos de la carrera {self.nombre}."
        return mensaje


class ObjetivoCarrera(Enum):
    EMPRENDIMIENTO = "Emprendimiento de empresas de investigación, innovación, desarrollo y comercialización de Software"
    DESARROLLO = "Ingeniería de Software para el desarrollo de Sistemas de Información y Sistemas Inteligentes"
    INVESTIGACION = "Investigación aplicada en proyectos de conceptualización, desarrollo, innovación y transferencia de Software"
    GESTION = "Administración de proyectos de Software"
    CALIDAD = "Verificación, validación y aseguramiento de la calidad del Software"


@step("que un estudiante pertenece a una carrera con (.+) objetivos")
def step_impl(context, arg0):
    """
    :type context: behave.runner.Context
    :type arg0: str
    """
    estudiante = Estudiante("Miguel", "Mendoza", 22, "202111108", "miguel.mendosa@epn.edu.ec")
    num_objetivos = int(arg0)
    todos_objetivos = list(ObjetivoCarrera)

    # Crear una instancia temporal de Carrera para validar los objetivos
    carrera_temp = Carrera("", 0, [])
    carrera_temp.validar_objetivos(num_objetivos, todos_objetivos)

    objetivos_seleccionados = todos_objetivos[:num_objetivos]

    # Crear asignaturas con los objetivos seleccionados
    asignatura1 = Asignatura("Verificación y Validación de Software",
                             [objetivos_seleccionados[0], objetivos_seleccionados[-1]])
    asignatura2 = Asignatura("Aplicaciones Móviles",
                             [objetivos_seleccionados[1], objetivos_seleccionados[0]])
    asignatura3 = Asignatura("USABILIDAD Y ACCESIBILIDAD",
                             [objetivos_seleccionados[-1], objetivos_seleccionados[1]])

    asignaturas = [asignatura1, asignatura2, asignatura3]

    # Crear la carrera con el número correcto de objetivos
    carrera = Carrera("Ingeniería de Software", num_objetivos, asignaturas)
    carrera.objetivos = objetivos_seleccionados

    estudiante.registrar_asignatura(asignatura1)
    estudiante.registrar_asignatura(asignatura2)
    carrera.matricular_estudiante(estudiante)

    context.estudiante = estudiante
    context.carrera = carrera

    assert estudiante.carrera is not None
    assert carrera.numero_de_objetivos == num_objetivos


@step("tiene registrado al menos un historial de perfil")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    estudiante = context.estudiante
    historial = estudiante.llenar_encuesta_del_semestre("2025-A", {
        estudiante.asignaturas[0]: [(estudiante.asignaturas[0].objetivos[0], 80),
                                    (estudiante.asignaturas[0].objetivos[1], 75)],
        estudiante.asignaturas[1]: [(estudiante.asignaturas[1].objetivos[0], 90),
                                    (estudiante.asignaturas[1].objetivos[1], 85)]
    })
    estudiante.registrar_semestre(historial)
    assert len(estudiante.historiales) >= 1


@step("el umbral de aceptación mínimo es de (?P<Umbral>.+) por ciento para cada objetivo")
def step_impl(context, Umbral):
    """
    :type context: behave.runner.Context
    :type Umbral: str
    """
    carrera = context.carrera
    carrera.establecer_umbral(int(Umbral))
    assert carrera.umbral_aceptacion == int(Umbral)


@step("el estudiante tiene un progreso por encima del umbral mínimo")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    estudiante = context.estudiante
    carrera = context.carrera

    assert (carrera.verificar_progreso_estudiante(estudiante)) is True


@step("consulte el progreso del historial")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    estudiante = context.estudiante
    carrera = context.carrera

    assert estudiante.obtener_progreso() is not None and isinstance(estudiante.obtener_progreso(), dict)



@step("mostrará el porcentaje de progreso por cada objetivo")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    estudiante = context.estudiante
    carrera = context.carrera
    progreso = estudiante.obtener_progreso()

    assert isinstance(progreso, dict) and all(isinstance(value, (float, int)) for value in progreso.values())
    assert all(0 <= value <= 100 for value in progreso.values())
    assert len(progreso) == len(carrera.objetivos)


@step("se mostrará la media de progreso de estudiantes")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    estudiante = context.estudiante
    carrera = context.carrera

    media_progreso = carrera.calcular_media_progreso()

    assert isinstance(media_progreso, dict)
    assert all(isinstance(value, float) for value in media_progreso.values())
    assert all(0 <= value <= 100 for value in media_progreso.values())
    assert len(media_progreso) == len(carrera.objetivos)  # Verificar contra los objetivos de la carrera


@step("un mensaje de felicitación")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    estudiante = context.estudiante
    carrera = context.carrera

    mensaje = carrera.mostrar_mensaje_felicitacion(estudiante)

    assert isinstance(mensaje, str)
    # Verificar que el mensaje contiene "¡Felicidades" (con el nombre)
    assert "¡Felicidades" in mensaje or "¡Buen trabajo" in mensaje
