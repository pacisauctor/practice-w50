CREATE TABLE users(
id_user serial primary key,
username varchar not null unique,
pass varchar not null,
email varchar not null
)

