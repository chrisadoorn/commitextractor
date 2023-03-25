set schema 'test';

-- procedures
DROP PROCEDURE IF EXISTS test.deregistreer_processor(character);
DROP PROCEDURE IF EXISTS test.registreer_processor(character, bigint);
DROP PROCEDURE IF EXISTS test.registreer_verwerking(bigint, character varying);
DROP PROCEDURE IF EXISTS test.verwerk_volgend_project(character, bigint, character varying, integer);

-- Tables
DROP TABLE IF EXISTS verwerk_project;
DROP TABLE IF EXISTS processor;
DROP TABLE IF EXISTS bestandswijziging;
DROP TABLE IF EXISTS commitinfo;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS selectie;
