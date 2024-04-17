import pandas as pd
from database import MySQLDatabase
import math

db = MySQLDatabase("localhost", "root", "", "analitics")

def obtener_anio_del_periodo(periodo):
    splitPeriodo = periodo.split(" ")
    return splitPeriodo[-1]

def obtener_estudiante(matricula):
    condition = "matricula = '" + str(matricula) + "'"
    estudianteEncontrado = db.read_records("estudiantes",['id'],condition)
    return estudianteEncontrado[0][0]

def obtener_periodo(periodo):
    condition = "periodo = '" + str(periodo) + "'"
    periodoEncontrado = db.read_records("periodos",['id'],condition)
    return periodoEncontrado[0][0]

def obtener_asignatura(asignatura):
    condition = "nombre = '" + str(asignatura.rstrip()) + "'"
    asignaturaEncontrada = db.read_records("asignaturas",['id'],condition)
    return asignaturaEncontrada[0][0]

def crear_estudiantes(parte):
    calificaciones = pd.read_excel(f"data/mapa_curricular/mapa_curricular_parte_{str(parte)}.xlsx")
    for _, calificacion in calificaciones.iterrows():
        matricula = calificacion['Matricula']
        condition = "matricula = '" + str(matricula) + "'"
        estudiante = db.read_records("estudiantes",['id','matricula'],condition)
        if len(estudiante) == 0 : 
            db.create_record(
                'estudiantes',
                ['matricula'],
                [matricula]
            )

def crear_periodos(parte):
    periodos = pd.read_excel(f"data/mapa_curricular/mapa_curricular_parte_{str(parte)}.xlsx")
    for _, periodo in periodos.iterrows():
        if not pd.isna(periodo["PeriodoCursado"]) : 
            periodo = periodo["PeriodoCursado"]
            anio = obtener_anio_del_periodo(periodo)
            condition = "periodo = '" + str(periodo) + "'"
            periodoEncontrado = db.read_records("periodos",['id','anio','periodo'],condition)
            if len(periodoEncontrado) == 0:
                db.create_record(
                    'periodos',
                    ['anio','periodo'],
                    [anio,periodo]
                )

def crear_calificaciones(parte):
    calificaciones = pd.read_excel(f"data/mapa_curricular/mapa_curricular_parte_{str(parte)}.xlsx")
    for _, calificacion in calificaciones.iterrows():
        extra = 0
        final = 0
        #SI NO LA HA CURSADO NO LA NECESITO
        if calificacion['EstatusMateria'] != 'Sin Cursar' and str(calificacion['PlanEstudiosClave']) == '4': 
            extra = -1 if math.isnan(calificacion['Extra']) else calificacion['Extra']
            final = -1 if math.isnan(calificacion['Final']) else calificacion['Final']

            print(f"SEGUIMIENTO: MATRICULA[{calificacion['Matricula']}] - PERIODO[{calificacion['PeriodoCursado']}] MATERIA[{calificacion['Materia']}]");

            estudiante = obtener_estudiante(calificacion['Matricula'])
            periodo    = obtener_periodo(calificacion['PeriodoCursado'])
            asignatura = obtener_asignatura(calificacion['Materia'])

            db.create_record(
                'calificaciones',
                ['cardex','extra','final','estudiante_id','periodo_id','asignatura_id'],
                [calificacion['EstatusCardex'],extra,final,estudiante,periodo,asignatura]
            )
print("PARTE 1")
crear_estudiantes(1)
crear_periodos(1)
crear_calificaciones(1)
print("======================")

print("PARTE 2")
crear_estudiantes(2)
crear_periodos(2)
crear_calificaciones(2)
print("======================")

print("PARTE 3")
crear_estudiantes(3)
crear_periodos(3)
crear_calificaciones(3)
print("======================")

print("PARTE 4")
crear_estudiantes(4)
crear_periodos(4)
crear_calificaciones(4)
print("======================")

