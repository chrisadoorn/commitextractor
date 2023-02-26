-- Database: multicore

-- DROP DATABASE IF EXISTS multicore;
-- for collation see: https://www.postgresql.org/docs/current/collation.html
-- We have chosen for full UTF-8 support.
CREATE DATABASE multicore
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT TEMPORARY, CONNECT ON DATABASE multicore TO PUBLIC;

GRANT TEMPORARY ON DATABASE multicore TO chris;

GRANT ALL ON DATABASE multicore TO postgres;