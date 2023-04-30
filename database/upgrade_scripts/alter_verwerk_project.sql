set schema test;

ALTER TABLE IF EXISTS verwerk_project
    RENAME start_extractie TO start_verwerking;

ALTER TABLE IF EXISTS verwerk_project
    RENAME einde_extractie TO einde_verwerking;

ALTER TABLE IF EXISTS verwerk_project
    ADD COLUMN processtap character varying;

DROP PROCEDURE IF EXISTS verwerk_volgend_project(character, bigint, character varying, integer);

UPDATE verwerk_project SET processtap = 'extractie';

-- run script 33_create_procedure_registreer_verwerking.sql
-- run script 34_create_procedure_verwerk_volgend_project.sql

