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

def convertir_formato_nombre_apellidos(nombre):
    nombres = nombre.split()

    if len(nombres) == 4:
        return f"{nombres[2]} {nombres[3]} {nombres[0]} {nombres[1]}"
    return f"{nombres[2]} {nombres[0]} {nombres[1]}"

def obtener_grupo(periodo,asignatura,docente,grupo):
    condition = f"periodo_id = '{periodo}' AND asignatura_id = '{asignatura}' AND docente_id = '{docente}' and grupo = '{grupo}'"
    grupo_encontrado = db.read_records("grupos", ['id'], condition)
    if len(grupo_encontrado) == 0 :
        return False
    return grupo_encontrado[0][0]

def obtener_estudiante(matricula):
    condition = "matricula = '" + str(matricula) + "'"
    estudianteEncontrado = db.read_records("estudiantes",['id'],condition)
    return estudianteEncontrado[0][0]

def obtener_calificacion(periodo,asignatura,estudiante):
    condition = f"periodo_id = '{periodo}' AND asignatura_id = '{asignatura}' AND estudiante_id = '{estudiante}'"
    calificacion_encontrada = db.read_records("calificaciones",['id'],condition)

    if len(calificacion_encontrada) == 0:
        return False
    return calificacion_encontrada[0][0]

def obtener_periodo(periodo):
    condition = "periodo = '" + str(periodo) + "'"
    periodoEncontrado = db.read_records("periodos",['id'],condition)
    return periodoEncontrado[0][0]

def obtener_asignatura(asignatura):
    condition = "nombre = '" + str(asignatura.rstrip()) + "'"
    asignaturaEncontrada = db.read_records("asignaturas",['id'],condition)
    return asignaturaEncontrada[0][0]

def obtener_persona(persona):
    condition = "nombre = '" + str(persona) + "'"
    docenteEncontrado = db.read_records("personas",['id'],condition)
    return docenteEncontrado[0][0]

def obtener_docente(persona):
    condition = "persona_id = '" + str(persona) + "'"
    docenteEncontrado = db.read_records("docentes",['id'],condition)
    return docenteEncontrado[0][0]

def asignar_calificaciones(archivo_grupo,grupo,periodo,asignatura,docente):
    docente = convertir_formato_nombre_apellidos(docente)
    asignatura = unicodedata.normalize('NFKD', asignatura).encode('ASCII', 'ignore').decode('utf-8')
    periodo = unicodedata.normalize('NFKD', periodo).encode('ASCII', 'ignore').decode('utf-8')
    docente = unicodedata.normalize('NFKD', docente).encode('ASCII', 'ignore').decode('utf-8')

    periodo = obtener_periodo(periodo)
    asignatura = obtener_asignatura(asignatura)
    persona = obtener_persona(docente)
    docente = obtener_docente(persona)

    grupo_encontrado = obtener_grupo(periodo,asignatura,docente,grupo)

    for _, alumno in archivo_grupo.iterrows():

        estudiante = obtener_estudiante(alumno['Matricula'])
        calificacion = obtener_calificacion(periodo,asignatura,estudiante)

        corte1 = -1 if pd.isna(alumno['P1']) else alumno['P1']
        corte2 = -1 if pd.isna(alumno['P2']) else alumno['P2']
        corte3 = -1 if pd.isna(alumno['P3']) else alumno['P3']
        recu1  = -1 if pd.isna(alumno['R1']) else alumno['R1']
        recu2  = -1 if pd.isna(alumno['R2']) else alumno['R2']
        recu3  = -1 if pd.isna(alumno['R3']) else alumno['R3']
        extra  = -1 if pd.isna(alumno['Extra']) else alumno['Extra']
        final   = -1 if pd.isna(alumno['Final']) else alumno['Final']

        if calificacion != False:
            condicion = f"id = '{calificacion}'"
            db.update_record(
                "calificaciones",
                {
                    "grupo_id":grupo_encontrado,
                    "ordinario_1":corte1, 
                    "ordinario_2":corte2,
                    "ordinario_3":corte3,
                    "recuperacion_1":recu1,
                    "recuperacion_2":recu2,
                    "recuperacion_3":recu3,
                    "extra":extra,
                    "final":final
                },
                condicion
            )

        if calificacion == False:
            campos = [
                'ordinario_1',
                'ordinario_2',
                'ordinario_3',
                'recuperacion_1',
                'recuperacion_2',
                'recuperacion_3',
                'extra',
                'final',
                'grupo_id',
                'estudiante_id',
                'periodo_id',
                'asignatura_id'
            ]

            valores = [
                corte1,
                corte2,
                corte3,
                recu1,
                recu2,
                recu3,
                extra,
                final,
                grupo_encontrado,
                estudiante,
                periodo, 
                asignatura
            ]

            db.create_record(
                'calificaciones',
                campos,
                valores
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

        asignar_calificaciones(
            archivo_grupo,
            grupo,
            periodo,
            asignatura,
            docente
        )