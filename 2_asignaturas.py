import sys
import os
import pandas as pd
from database import MySQLDatabase

from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name    = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")

db = MySQLDatabase(db_host,db_user,db_password,db_name,db_port)

def crear_asignaturas():
    materias = pd.read_excel('data/materias/MateriasIDS.xlsx')
    for _, materia in materias.iterrows():
        db.create_record(
            'asignaturas',
            ['nombre','abreviatura','creditos','cuatrimestre','order_grafico','horas_semana','total_horas','plan_id'],
            [materia['Nombre'].rstrip(),materia['Abreviatura'],materia['Creditos'],materia['Periodo'],materia['OrdenGrafico'],materia['HorasSemana'],materia['TotalHoras'],1]
        )


crear_asignaturas()
