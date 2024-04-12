import pandas as pd
from database import MySQLDatabase
import math

db = MySQLDatabase("localhost", "root", "", "analitics")

def ob_crear_estudiante(matricula):
    print(matricula)
    condition = "matricula ="+str(matricula)
    estudiante = db.read_records("estudiantes",['id','matricula'],condition)
 
    if len(estudiante) == 0 : 
        estudiante = db.create_record(
            'estudiantes',
            ['matricula'],
            [matricula]
        )
    else:
        return estudiante[0][0]

def crear_estudiantes():
    calificaciones = pd.read_excel("data/mapa_curricular/mapa_curricular_parte_2.xlsx")
    for _, calificacion in calificaciones.iterrows():
        ob_crear_estudiante(calificacion['Matricula'])

def crear_calificaciones():
    calificaciones = pd.read_excel("data/mapa_curricular/mapa_curricular_parte_1.xlsx")
    for _, calificacion in calificaciones.iterrows():

        extra = 0
        final = 0

        if math.isnan(calificacion['Extra']) == False: 
            extra = calificacion['Extra']

        if math.isnan(calificacion['Final']) == False:
            final = calificacion['Final']

        estudiante = ob_crear_estudiante(calificacion['Matricula'])
        
        db.create_record(
            'calificaciones',
            ['cardex','extra','final','estudiante_id'],
            [calificacion['EstatusCardex'],extra,final,estudiante]
        )

crear_estudiantes()
#crear_calificaciones()

