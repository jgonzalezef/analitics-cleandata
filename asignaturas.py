import sys
import pandas as pd
from database import MySQLDatabase

db = MySQLDatabase("localhost", "root", "", "analitics")

def crear_asignaturas():
    materias = pd.read_excel('data/materias/MateriasIDS.xlsx')
    for _, materia in materias.iterrows():
        db.create_record(
            'asignaturas',
            ['nombre','abreviatura','creditos','cuatrimestre','order_grafico','horas_semana','total_horas','plan_id'],
            [materia['Nombre'],materia['Abreviatura'],materia['Creditos'],materia['Periodo'],materia['OrdenGrafico'],materia['HorasSemana'],materia['TotalHoras'],1]
        )


crear_asignaturas()
