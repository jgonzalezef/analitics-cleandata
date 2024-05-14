#RETICULA
select
	asignaturas.id,
	asignaturas.nombre,
	asignaturas.creditos,
	asignaturas.cuatrimestre,
	CASE 
		WHEN calificaciones.estatus_asignatura IS NOT NULL THEN calificaciones.estatus_asignatura
		ELSE 'Cursando'
	END AS estatus_asignatura
	
from asignaturas
left join calificaciones on asignaturas.id = calificaciones.asignatura_id
inner join estudiantes on calificaciones.estudiante_id = estudiantes.id
where estudiantes.matricula  = "211102"
union 
select 
	asignaturas.id,
	asignaturas.nombre,
	asignaturas.creditos,
	asignaturas.cuatrimestre,
	'Pendiente' as estatus_asignatura
from asignaturas

where id not in (
	select asignatura_id  from calificaciones where estudiante_id = (
		select id from estudiantes where matricula ="211102"
	)
)


#INFORMACION POR COHORTE
SELECT 
	count(*) as numero_estudiantes,
	left(matricula,3) as cohorte,
	(
		select 
			count(*) as titulados 
		from estudiantes where estatus = 'Titulado' and 
		left(matricula,3) = cohorte

	) as titulados,
	(
		select 
			count(*) as titulados 
		from estudiantes where estatus = 'Proceso Titulación' and 
		left(matricula,3) = cohorte

	) as proceso_titulacion
FROM estudiantes
group by left(matricula,3);