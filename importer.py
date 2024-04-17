# Importa los scripts
import subprocess

# Ejecuta los archivos en orden
subprocess.run(["python3", "1_planes.py"])
subprocess.run(["python3", "2_asignaturas.py"])
subprocess.run(["python3", "3_calificaciones.py"])
subprocess.run(["python3", "5_docentes.py"])
subprocess.run(["python3", "6_grupos.py"])
subprocess.run(["python3", "7_calificaciones_grupos.py"])
subprocess.run(["python3", "8_tutores.py"])
subprocess.run(["python3", "9_estudiante_persona.py"])
subprocess.run(["python3", "10_estudiantes_estatus.py"])
subprocess.run(["python3", "11_estudiantes_cuatrimestre.py"])