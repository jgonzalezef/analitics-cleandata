import sys
import pandas as pd
from database import MySQLDatabase

db = MySQLDatabase("localhost", "root", "", "analitics")


def crear_plan():
    planes = pd.read_excel('data/planes/PlanDeEstudiosIDS.xlsx')
    for _, plan in planes.iterrows():
        db.create_record('planes',['nombre','creditos'],[plan['Clave'],plan['Creditos']])

crear_plan()
