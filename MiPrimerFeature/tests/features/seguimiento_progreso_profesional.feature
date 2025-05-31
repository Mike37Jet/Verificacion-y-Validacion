# Created by migue at 27/5/2025
# language: es

Característica: Seguimiento de autoevaluación de progreso profesional
  Como estudiante de la EPN
  Quiero conocer mi progreso profesional a lo largo de cada semestre en relación a los objetivos de carrera
  Para determinar posibles falencias en mi proceso académico y tomar acciones correctivas

  Antecedentes:
    Dado que el estudiante tiene registrado al menos un historial de perfil estudiantil

  Escenario: Seguimiento sin falencias
    Y la carrera de sistemas tiene los siguientes objetivos:
      | Verificación, validación y aseguramiento de la calidad del Software |
      | Administración de proyectos de Software |
      | Investigación aplicada en proyectos de conceptualización, desarrollo, innovación y transferencia de Software |
      | Ingeniería de Software para el desarrollo de Sistemas de Información y Sistemas Inteligentes |
      | Emprendimiento de empresas de investigación, innovación, desarrollo y comercialización de Software |
    # Aprender
    Cuando consulte el progreso del historial
    Entonces mostrará un porcentaje de progreso por cada objetivo
    #feature_seguimineto_001
    Y se mostrará la media de progreso de estudiantes

    #Tarea - Leer documentación Cucumber
  Escenario: Seguimiento con falencias
    Y el umbral de aceptación mínimo es de 70
    Cuando consulte el progreso del historial
    Entonces mostrará un porcentaje de progreso por cada objetivo
    #feature_seguimineto_001
    Y se mostrará la media de progreso de estudiantes
    Y se mostrará una serie de recomendaciones para mejorar el progreso