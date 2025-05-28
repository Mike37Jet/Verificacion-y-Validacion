# Created by migue at 27/5/2025
# language: es

Característica: Seguimiento de autoevaluación de progreso profesionalizante
  Como estudiante de la EPN
  Quiero conocer mi progreso profesional a lo largo de cada semestre en relación a los objetivos de carrera
  Para determinar posibles falencias en mi proceso académico y tomar acciones correctivas

  Antecedentes:
    Dado que el estudiante tiene registrado almenos un historial de perfil estudiantil

  Escenario: Seguimiento sin falencias
    Y el umbrar de aceptación mínimo es de 70
    Y  la carrera de sistemas tienes los siguientes objetivos:
        | Objetivo |
        | Aprender a programar en Python |
        | Desarrollar aplicaciones web |
    # Aprender
    Cuando consulte el progreso del historial
    Entonces mostrará un porcentaje de progreso por cada objetivo
    #feature_seguimineto_001
    Y se mostrará la media de progreso de estudiantes

    #Tarea - Leer documentación Cucumber
  Escenario: Seguimiento con falencias
    Y el umbrar de aceptación mínimo es de 70
    Cuando consulte el progreso del historial
    Entonces mostrará un porcentaje de progreso por cada objetivo
    #feature_seguimineto_001
    Y se mostrará la media de progreso de estudiantes
    Y se mostrará una serie de recomendaciones para mejorar el progreso