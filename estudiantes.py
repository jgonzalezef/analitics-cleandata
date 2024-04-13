import pandas as pd
from database import MySQLDatabase
import math

db = MySQLDatabase("localhost", "root", "13960", "analitics")


     #data\mapa_curricular\mapa_curricular_parte_1.xlsx
    #data\mapa_curricular\mapa_curricular_parte_2.xlsx
    #data\mapa_curricular\mapa_curricular_parte_3.xlsx
    #data\mapa_curricular\mapa_curricular_parte_4.xlsx


def obtener_anio_del_periodo(periodo):
    splitPeriodo = periodo.split(" ")
    return splitPeriodo[-1]

def obtener_estudiante(matricula):
    condition = "matricula ="+str(matricula)
    estudiante = db.read_records("estudiantes",['id'],condition)
    return estudiante[0][0]

def crear_estudiantes():
    for i in range(1, 5):
        calificaciones = pd.read_excel(f"data/mapa_curricular/mapa_curricular_parte_{i}.xlsx")
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

def crear_periodos():
    for i in range(1, 5):
        periodos = pd.read_excel(f"data/mapa_curricular/mapa_curricular_parte_{i}.xlsx")
        for _, periodo in periodos.iterrows():
            if math.isnan(periodo['Extra']) == False and math.isnan(periodo['Final']) == False:
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

#TODO: VERIFICAR ERROR: Error executing query: 1054 (42S22): Unknown column 'nan' in 'field list'
def crear_calificaciones():
    for i in range(1, 5):
        calificaciones = pd.read_excel(f"data/mapa_curricular/mapa_curricular_parte_{i}.xlsx")
        for _, calificacion in calificaciones.iterrows():
            extra = 0
            final = 0
            if math.isnan(calificacion['Extra']) == False: 
                extra = calificacion['Extra']
            if math.isnan(calificacion['Final']) == False:
                final = calificacion['Final']
            estudiante = obtener_estudiante(calificacion['Matricula'])
            db.create_record(
                'calificaciones',
                ['cardex','extra','final','estudiante_id'],
                [calificacion['EstatusCardex'],extra,final,estudiante]
            )


crear_periodos()
crear_estudiantes()
crear_calificaciones()


