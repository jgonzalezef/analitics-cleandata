import os
import pandas as pd
from database import MySQLDatabase

db = MySQLDatabase("localhost", "root", "", "analitics","3306")

directorio = 'data/mapa_curricular'

def obtener_estudiante(matricula):
    condition = "matricula = '" + str(matricula) + "'"
    estudianteEncontrado = db.read_records("estudiantes", ['id'], condition)
    return estudianteEncontrado[0][0]

for archivo in os.listdir(directorio):
    if archivo.endswith('.xlsx'):
        ruta_archivo = os.path.join(directorio, archivo)
        mapa_curricular = pd.read_excel(ruta_archivo)
        mapa_curricular.sort_values(by=['Matricula'], inplace=True)
        ultimo_estatus_por_matricula = mapa_curricular.groupby('Matricula').last().reset_index()
        for _, alumno in ultimo_estatus_por_matricula.iterrows():
            condicion = f"matricula = '{alumno['Matricula']}'"
            db.update_record(
                "estudiantes",
                {
                    "cuatrimestre_actual":alumno['CuatrimestreActual']
                },
                condicion
            )