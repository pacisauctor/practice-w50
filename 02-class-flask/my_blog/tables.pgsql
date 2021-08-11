
-- creando esquema
create schema flask;

-- creando tabla
CREATE TABLE flask.post(
    id serial primary key,
    autor varchar not null, 
    titulo varchar not null,
    contenido varchar not null
)