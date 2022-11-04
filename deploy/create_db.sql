DROP DATABASE IF EXISTS sgp_db;

CREATE DATABASE sgp_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_PY.UTF-8'
    LC_CTYPE = 'es_PY.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
