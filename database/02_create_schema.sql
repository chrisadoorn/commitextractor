-- definieer 2 schema's
--  voor ontwikkelen
--  voor verwerking
-- SCHEMA: test

-- DROP SCHEMA IF EXISTS test ;

CREATE SCHEMA IF NOT EXISTS test
    AUTHORIZATION appl;

GRANT ALL ON SCHEMA test TO appl;

-- SCHEMA: prod

-- DROP SCHEMA IF EXISTS prod ;

CREATE SCHEMA IF NOT EXISTS prod
    AUTHORIZATION appl;

GRANT ALL ON SCHEMA prod TO appl;