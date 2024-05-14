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


def crear_plan():
    planes = pd.read_excel('data/planes/PlanDeEstudiosIDS.xlsx')
    for _, plan in planes.iterrows():
        db.create_record('planes',['nombre','creditos'],[plan['Clave'],plan['Creditos']])

crear_plan()
