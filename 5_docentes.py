import os
import pandas as pd
from database import MySQLDatabase
import unicodedata
from tabulate import tabulate

db = MySQLDatabase("localhost", "root", "", "analitics")
directorio = 'data/grupos'

ASIGNATURA_POSICION = 0
GRUPO_POSICION = 1
DOCENTE_POSICION = 2
PERIODO_POSICION = 3

docentes = set()

def convertir_formato_nombre_apellidos(nombre):
    nombres = nombre.split()

    if len(nombres) == 4:
        return f"{nombres[2]} {nombres[3]} {nombres[0]} {nombres[1]}"
    return f"{nombres[2]} {nombres[0]} {nombres[1]}"

def obtener_persona(persona):
    condition = "nombre = '" + str(persona) + "'"
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

def obtener_docente(persona):
    condition = "persona_id = '" + str(persona) + "'"
    docenteEncontrado = db.read_records("docentes",['id'],condition)
    if len(docenteEncontrado) == 0:
        return False
    return docenteEncontrado[0][0]

def asignar_persona_docente(persona):
    if obtener_docente(persona) == False:
        db.create_record(
            'docentes',
            ['persona_id'],
            [persona]
        )

def crear_docentes(docentes):
    for docente in docentes:
        persona_encontrada = obtener_persona(docente)
        if persona_encontrada == False:
            crear_persona(docente)
        persona_encontrada = obtener_persona(docente)
        asignar_persona_docente(persona_encontrada)

for archivo in os.listdir(directorio):
    if archivo.endswith('.xlsx'):
        nombre_archivo = os.path.basename(archivo)
        archivo_grupo = pd.read_excel(os.path.join(directorio, archivo))
        tokens = nombre_archivo.split(' - ')
        docente_grupo = tokens[DOCENTE_POSICION]
        docente_grupo = convertir_formato_nombre_apellidos(docente_grupo)
        docentes.add(unicodedata.normalize('NFKD', docente_grupo).encode('ASCII', 'ignore').decode('utf-8'))
        for _, alumno in archivo_grupo.iterrows():
            if not pd.isna(alumno['Tutor']):
                docentes.add(unicodedata.normalize('NFKD', alumno['Tutor']).encode('ASCII', 'ignore').decode('utf-8'))

crear_docentes(docentes)
    
