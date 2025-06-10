# Created by Miguel Mendosa at 27/5/2025
# language: es

Característica: Seguimiento de autoevaluación de progreso profesional
  Como estudiante de la EPN
  Quiero conocer mi progreso profesional a lo largo de cada semestre en relación a los objetivos de carrera
  Para determinar posibles falencias en mi proceso académico y tomar acciones correctivas

  Esquema del escenario: Seguimiento sin falencias
    Dado que un estudiante pertenece a una carrera con <Número de objetivos> objetivos
    Y tiene registrado al menos un historial de perfil
    Y el umbral de aceptación mínimo es de <Umbral> por ciento para cada objetivo
    Y el estudiante tiene un progreso por encima del umbral mínimo
    Cuando consulte el progreso del historial
    Entonces mostrará el porcentaje de progreso por cada objetivo
    Y se mostrará la media de progreso de estudiantes
    Y un mensaje de felicitación
    Ejemplos:
      | Número de objetivos   | Umbral          |
      | 5 | 70 |
    #  | 3 | 70 |
     # | 5 | 90 |
      #| 5 | -70 |















