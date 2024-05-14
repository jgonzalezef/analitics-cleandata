import os
import pandas as pd
from database import MySQLDatabase
import math
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name    = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")

db = MySQLDatabase(db_host,db_user,db_password,db_name,db_port)

directorio = 'data/grupos'

ASIGNATURA_POSICION = 0
GRUPO_POSICION = 1
DOCENTE_POSICION = 2
PERIODO_POSICION = 3

def obtener_estudiante(matricula):
    condition = "matricula = '" + str(matricula) + "'"
    estudianteEncontrado = db.read_records("estudiantes",['id'],condition)
    return estudianteEncontrado[0][0]

def obtener_persona(persona):
    condition = "nombre = '" + str(persona) + "'"
    docenteEncontrado = db.read_records("personas",['id'],condition)
    return docenteEncontrado[0][0]

def obtener_docente(persona):
    condition = "persona_id = '" + str(persona) + "'"
    docenteEncontrado = db.read_records("docentes",['id'],condition)
    return docenteEncontrado[0][0]

def asignar_tutores(archivo_grupo):
    for _, alumno in archivo_grupo.iterrows():
        if not pd.isna(alumno['Tutor']):
            persona = obtener_persona(alumno['Tutor'])
            docente = obtener_docente(persona)

            condicion = f"matricula = '{alumno['Matricula']}'"
            db.update_record(
                "estudiantes",
                {
                    "tutor_academico_id":docente
                },
                condicion
            )



for archivo in os.listdir(directorio):
    if archivo.endswith('.xlsx'):
        nombre_archivo = os.path.basename(archivo)
        archivo_grupo = pd.read_excel(os.path.join(directorio, archivo))
        asignar_tutores(archivo_grupo)