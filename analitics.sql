#RESTANTE
create table personas(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido_paterno VARCHAR(50) NULL,
    apellido_materno VARCHAR(50) NULL,
    telefono VARCHAR(50) NULL,
    curp VARCHAR(18) NULL,
    sexo VARCHAR(1) NULL
);

#RESTANTE
create table direcciones (
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	codigo_postal VARCHAR(10),
    ciudad VARCHAR(255),
    colonia VARCHAR(255),
    numero_interior VARCHAR(50),
    numero_exterior VARCHAR(50),
    calle_1 VARCHAR(255) NULL,
    calle_2 VARCHAR (255) NULL,
    referencias_direccion TEXT NULL,
    persona_id BIGINT UNSIGNED,
    FOREIGN KEY (persona_id) REFERENCES personas(id)
);

#RESTANTES
create table periodos(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    anio VARCHAR(10),
    periodo VARCHAR(100)
);

#RESTANTES
create table docentes(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    persona_id  BIGINT UNSIGNED,
    FOREIGN KEY (persona_id) REFERENCES personas(id)
);

#RESTANTES
#ESTATUS:INSCRITO,BAJA_DEFINITIVA,BAJA_ACADEMICA,TITULADO
create table estudiantes(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(20) UNIQUE,
    estatus VARCHAR(20),
    persona_id BIGINT UNSIGNED,
    perido_id BIGINT UNSIGNED,
    tutor_academico_id  BIGINT UNSIGNED NULL,
    tuto_familiar_id BIGINT UNSIGNED NULL,
    FOREIGN KEY (persona_id) REFERENCES personas(id),
    FOREIGN KEY (perido_id) REFERENCES periodos(id),
    FOREIGN KEY (tutor_academico_id) REFERENCES docentes(id),
    FOREIGN KEY (tuto_familiar_id) REFERENCES personas(id)
);

#ESTATUS:INSCRITO,BAJA_DEFINITIVA,BAJA_ACADEMICA,TITULADO
#RESTANTES
create table historial_estatus_estudiantes(
	estudiante_id BIGINT UNSIGNED,
	estatus VARCHAR(20) CHECK (estatus IN ('INSCRITO', 'BAJA_DEFINITIVA', 'BAJA_ACADEMICA', 'TITULADO')),
	FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id)
);

#LISTO
create table planes(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    creditos INTEGER
);

#LISTO
create table asignaturas(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    abreviatura VARCHAR(10),
    creditos INT,
    cuatrimestre VARCHAR(50),
    order_grafico INT,
    horas_semana INT,
    total_horas INT,
    plan_id BIGINT UNSIGNED,
    FOREIGN KEY (plan_id) REFERENCES planes(id)
);

#RESTANTES
create table grupos(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    grupo varchar(20),
    periodo_id  BIGINT UNSIGNED ,
    asignatura_id BIGINT UNSIGNED,
    docente_id BIGINT UNSIGNED NULL,
    FOREIGN KEY (periodo_id) REFERENCES periodos(id),
    FOREIGN KEY (asignatura_id) REFERENCES asignaturas(id),
    FOREIGN KEY (docente_id) REFERENCES docentes(id)
);

#RESTANTES
create table calificaciones(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ordinario_1 DOUBLE NULL,
    ordinario_2 DOUBLE NULL,
    ordinario_3 DOUBLE NULL,
    recuperacion_1 DOUBLE NULL,
    recuperacion_2 DOUBLE NULL,
    recuperacion_3 DOUBLE NULL,
    cardex VARCHAR(50),
    extra DOUBLE NULL,
    final DOUBLE NULL,
    grupo_id BIGINT UNSIGNED NULL,
    estudiante_id BIGINT UNSIGNED NULL,
    periodo_id BIGINT UNSIGNED NULL,
    asignatura_id BIGINT UNSIGNED NULL,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id),
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
    FOREIGN KEY (periodo_id) REFERENCES periodos(id),
    FOREIGN KEY (asignatura_id) REFERENCES asignaturas(id)
);

create table roles(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(50)
);

create table usuarios(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(50),
	password VARCHAR (50),
	role_id BIGINT UNSIGNED,
	FOREIGN KEY (role_id) REFERENCES roles(id)
);

create table permisos(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(50)
);

create table modulos(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(50)
);

create table roles_permisos(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	role_id BIGINT UNSIGNED,
	permiso_id BIGINT UNSIGNED,
	FOREIGN KEY (role_id) REFERENCES roles(id),
	FOREIGN KEY (permiso_id) REFERENCES permisos(id)
);

create table roles_modulos_permisos(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	role_id BIGINT UNSIGNED,
	permiso_id BIGINT UNSIGNED,
	modulo_id BIGINT UNSIGNED,
	FOREIGN KEY (role_id) REFERENCES roles(id),
	FOREIGN KEY (permiso_id) REFERENCES permisos(id),
	FOREIGN KEY (modulo_id) REFERENCES modulos(id)
);


#OBTENER MATERIAS DE UN ESTUDIANTE
select
	periodos.periodo,
	periodos.anio as periodo_año,
	asignaturas.nombre as asignatura,
	asignaturas.cuatrimestre as asignatura_cuatrimestre,
	asignaturas.creditos as asignatura_creditos_logrados,
	calificaciones.cardex,
	calificaciones.ordinario_1 as corte1,
	calificaciones.ordinario_2 as corte2,
	calificaciones.ordinario_3 as corte2,
	calificaciones.recuperacion_1 as recu1,
	calificaciones.recuperacion_2 as recu2,
	calificaciones.recuperacion_3 as recu3,
	calificaciones.final as calificacion_final,
	calificaciones.extra as calificacion_extraordinaria
from calificaciones
inner join periodos on calificaciones.periodo_id  = periodos.id
inner join asignaturas on calificaciones.asignatura_id = asignaturas.id
where calificaciones.estudiante_id = (
	select id from estudiantes where matricula ="211105"
);

#OBTENER MATERIAS NO CURSADAS
select * from asignaturas where id not in (
	select asignatura_id  from calificaciones where estudiante_id = (
		select id from estudiantes where matricula ="211105"
	)
);

#Obtener datos de los grupos
select
	personas.nombre as docente,
	asignaturas.nombre as asignatura,
	asignaturas.cuatrimestre as asignatura_cuatrimestre,
	periodos.periodo,
	periodos.anio as periodo_año
from grupos 
inner join docentes on grupos.docente_id = docentes.id
inner join personas on docentes.persona_id  = personas.id
inner join asignaturas on grupos.asignatura_id = asignaturas.id
inner join periodos on grupos.periodo_id = periodos.id
order by 
	asignaturas.nombre asc,
	asignaturas.cuatrimestre asc

#obtener datos de los estudiantes con tutores
select 
	estudiantes.id as estudiante_id,
	estudiantes.matricula,
	estudiantes_persona.nombre,
	docentes.id as docente_id,
	personas.nombre
from estudiantes 
inner join docentes on estudiantes.tutor_academico_id  = docentes.id
inner join personas on docentes.persona_id  = personas.id
inner join personas as estudiantes_persona on estudiantes.persona_id = estudiantes_persona.id
where estudiantes.tutor_academico_id is not null and estudiantes.matricula = "211262";