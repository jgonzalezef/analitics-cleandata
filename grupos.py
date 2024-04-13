import os
import pandas as pd
from database import MySQLDatabase

db = MySQLDatabase("localhost", "root", "", "analitics")

directorio = 'data/grupos'
datos_totales = []

ASIGNATURA_POSICION = 0
GRUPO_POSICION = 1
DOCENTE_POSICION = 2
PERIODO_POSICION = 3

def obtener_persona_docente(docente):
    condition = "nombre = '" + str(docente) + "'"
    docenteEncontrado = db.read_records("personas",['id'],condition)
    if len(docenteEncontrado) == 0:
        return False
    return docenteEncontrado[0][0]

def crear_persona(persona):
    db.create_record(
        'personas',
        ['nombre'],
        [persona]
    )

def asignar_persona_docente(persona):
    db.create_record(
        'docentes',
        ['persona_id'],
        [persona]
    )

def crear_personas_docentes(archivo_grupo,docente_grupo):
    for _, alumno in archivo_grupo.iterrows():
        if obtener_persona_docente(alumno['Tutor']) == False:
            crear_persona(alumno['Tutor'])

for archivo in os.listdir(directorio):
    if archivo.endswith('.xlsx'):
        nombre_archivo = os.path.basename(archivo)
        tokens = nombre_archivo.split(' - ')

        grupo  = tokens[GRUPO_POSICION]
        asignatura = tokens[ASIGNATURA_POSICION]
        docente_grupo  = tokens[DOCENTE_POSICION]
        periodo  = tokens[PERIODO_POSICION].replace(".xlsx","")
        
        archivo_grupo    = pd.read_excel(os.path.join(directorio,archivo))

        if obtener_persona_docente(docente_grupo) == False:
            crear_persona(docente_grupo)

        crear_personas_docentes(archivo_grupo,docente_grupo)

        # cargar_grupos(
        #     archivo_grupo,
        #     grupo,
        #     asignatura,
        #     docente,
        #     periodo
        # )