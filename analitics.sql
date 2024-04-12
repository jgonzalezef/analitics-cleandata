#RESTANTE
create table personas(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido_paterno VARCHAR(50),
    apellido_materno VARCHAR(50),
    telefono VARCHAR(50) NULL,
    curp VARCHAR(18) NULL,
    sexo VARCHAR(1)
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

create table cat_periodos(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	periodo VARCHAR(50)
);

#RESTANTES
create table periodos(
	id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    anio INT UNSIGNED,
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
    estatus VARCHAR(20) CHECK (estatus IN ('INSCRITO', 'BAJA_DEFINITIVA', 'BAJA_ACADEMICA', 'TITULADO')),
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
    cardex VARCHAR(50) CHECK (cardex IN ('Ordinario', 'Repeticion', 'Especial', 'Equivalencia')),
    extra DOUBLE,
    final DOUBLE,
    grupo_id BIGINT UNSIGNED NULL,
    estudiante_id BIGINT UNSIGNED,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id),
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id)
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

