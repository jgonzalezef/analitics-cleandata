import os
import pandas as pd
from database import MySQLDatabase
from tabulate import tabulate
import unicodedata
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

alumnos = []

def convertir_formato_nombre_apellidos(nombre):
    nombres = nombre.split()

    if len(nombres) == 4:
        return f"{nombres[2]} {nombres[3]} {nombres[0]} {nombres[1]}"
    return f"{nombres[2]} {nombres[0]} {nombres[1]}"

def obtener_asignatura(asignatura):
    condition = "nombre = '" + str(asignatura.rstrip()) + "'"
    asignaturaEncontrada = db.read_records("asignaturas",['id'],condition)
    return asignaturaEncontrada[0][0]

def obtener_periodo(periodo):
    condition = "periodo = '" + str(periodo) + "'"
    periodoEncontrado = db.read_records("periodos",['id'],condition)
    return periodoEncontrado[0][0]

def obtener_docente(persona):
    condition = "persona_id = '" + str(persona) + "'"
    docenteEncontrado = db.read_records("docentes",['id'],condition)
    return docenteEncontrado[0][0]

def obtener_persona(persona):
    condition = "nombre = '" + str(persona) + "'"
    docenteEncontrado = db.read_records("personas",['id'],condition)
    return docenteEncontrado[0][0]

def obtener_grupo(periodo,asignatura,docente,grupo):
    condition = f"periodo_id = '{periodo}' AND asignatura_id = '{asignatura}' AND docente_id = '{docente}' and grupo = '{grupo}'"
    grupo_encontrado = db.read_records("grupos", ['id'], condition)
    if len(grupo_encontrado) == 0 :
        return False
    return grupo_encontrado[0][0]

def crear_grupo(grupo,periodo,asignatura,docente):
    docente = convertir_formato_nombre_apellidos(docente)
    asignatura = unicodedata.normalize('NFKD', asignatura).encode('ASCII', 'ignore').decode('utf-8')
    periodo = unicodedata.normalize('NFKD', periodo).encode('ASCII', 'ignore').decode('utf-8')
    docente = unicodedata.normalize('NFKD', docente).encode('ASCII', 'ignore').decode('utf-8')

    periodo = obtener_periodo(periodo)
    asignatura = obtener_asignatura(asignatura)
    persona = obtener_persona(docente)
    docente = obtener_docente(persona)

    grupo_encontrado = obtener_grupo(
        periodo,
        asignatura,
        docente,
        grupo
    )

    if grupo_encontrado == False :
        db.create_record(
            'grupos',
            ['grupo','periodo_id','asignatura_id','docente_id'],
            [grupo,periodo,asignatura,docente]
        )

ASIGNATURA_POSICION = 0
GRUPO_POSICION = 1
DOCENTE_POSICION = 2
PERIODO_POSICION = 3

for archivo in os.listdir(directorio):
    if archivo.endswith('.xlsx'):
        nombre_archivo = os.path.basename(archivo)
        archivo_grupo = pd.read_excel(os.path.join(directorio, archivo))
        tokens = nombre_archivo.split(' - ')
        asignatura = tokens[ASIGNATURA_POSICION]
        grupo = tokens[GRUPO_POSICION]
        docente = tokens[DOCENTE_POSICION]
        periodo  = tokens[PERIODO_POSICION].replace(".xlsx","")

        crear_grupo(
            grupo,
            periodo,
            asignatura,
            docente
        )