-- Database: multicore

-- DROP DATABASE IF EXISTS multicore;

CREATE DATABASE multicore
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Dutch_Netherlands.1252'
    LC_CTYPE = 'Dutch_Netherlands.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT TEMPORARY, CONNECT ON DATABASE multicore TO PUBLIC;

GRANT TEMPORARY ON DATABASE multicore TO chris;

GRANT ALL ON DATABASE multicore TO postgres;