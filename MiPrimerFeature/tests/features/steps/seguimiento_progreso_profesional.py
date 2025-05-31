from behave import *

use_step_matcher("re")


@step("que el estudiante tiene registrado al menos un historial de perfil estudiantil")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Dado que el estudiante tiene registrado al menos un historial de perfil estudiantil')


@step("la carrera de sistemas tiene los siguientes objetivos:")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u"""STEP: Y la carrera de sistemas tiene los siguientes objetivos:
        | Verificación, validación y aseguramiento de la calidad del Software |
        | Administración de proyectos de Software |
        | Investigación aplicada en proyectos de conceptualización, desarrollo, innovación y transferencia de Software |
        | Ingeniería de Software para el desarrollo de Sistemas de Información y Sistemas Inteligentes |
        | Emprendimiento de empresas de investigación, innovación, desarrollo y comercialización de Software |
        """
    )

@step("consulte el progreso del historial")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Cuando consulte el progreso del historial')


@step("mostrará un porcentaje de progreso por cada objetivo")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Entonces mostrará un porcentaje de progreso por cada objetivo')


@step("se mostrará la media de progreso de estudiantes")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Y se mostrará la media de progreso de estudiantes')


@step("el umbral de aceptación mínimo es de 70")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Y el umbral de aceptación mínimo es de 70')


@step("se mostrará una serie de recomendaciones para mejorar el progreso")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Y se mostrará una serie de recomendaciones para mejorar el progreso')