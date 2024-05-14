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

def convertir_formato_nombre_apellidos(nombre):
    nombres = nombre.split()

    if len(nombres) == 4:
        return f"{nombres[2]} {nombres[3]} {nombres[0]} {nombres[1]}"
    return f"{nombres[2]} {nombres[0]} {nombres[1]}"

def obtener_estudiante(matricula):
    condition = "matricula = '" + str(matricula) + "'"
    estudianteEncontrado = db.read_records("estudiantes",['id'],condition)
    return estudianteEncontrado[0][0]

def obtener_persona(persona):
    condition = "nombre = '" + str(persona) + "'"
    docenteEncontrado = db.read_records("personas",['id'],condition)
    if len(docenteEncontrado) == 0:
        return False
    return docenteEncontrado[0][0]

def asignar_persona_alumno_por_nombre(nombre_persona,matricula):
    persona = obtener_persona(nombre_persona)
    condicion = f"matricula = '{matricula}'"
    db.update_record(
        "estudiantes",
        {
            "persona_id":persona
        },
        condicion
    )
    
def asignar_persona_alumno_por_persona_id(persona,matricula):
    condicion = f"matricula = '{matricula}'"
    db.update_record(
        "estudiantes",
        {
            "persona_id":persona
        },
        condicion
    )

def datos_personales(archivo_grupo):
    for _, alumno in archivo_grupo.iterrows():
        if not pd.isna(alumno['Nombre']):

            persona = obtener_persona(alumno['Nombre'])

            print(persona)

            if persona == False:
                alumno_nombre = convertir_formato_nombre_apellidos(alumno['Nombre'])
                db.create_record(
                    "personas",
                    ['nombre'],
                    [alumno_nombre]
                )
                asignar_persona_alumno_por_nombre(alumno_nombre,alumno['Matricula'])
            else:
                asignar_persona_alumno_por_persona_id(persona,alumno['Matricula'])

for archivo in os.listdir(directorio):
    if archivo.endswith('.xlsx'):
        nombre_archivo = os.path.basename(archivo)
        archivo_grupo = pd.read_excel(os.path.join(directorio, archivo))
        datos_personales(archivo_grupo)