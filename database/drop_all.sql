set schema 'test';

-- procedures
DROP PROCEDURE IF EXISTS deregistreer_processor(character);
DROP PROCEDURE IF EXISTS registreer_processor(character, bigint);
DROP PROCEDURE IF EXISTS registreer_verwerking(bigint, character varying);
DROP PROCEDURE IF EXISTS verwerk_volgend_project(character, bigint, character varying, integer);

-- Tables
DROP TABLE IF EXISTS verwerk_project;
DROP TABLE IF EXISTS verwerking_geschiedenis;
DROP TABLE IF EXISTS processor;
DROP TABLE IF EXISTS bestandswijziging_zoekterm;
DROP TABLE IF EXISTS bestandswijziging_info;
DROP TABLE IF EXISTS bestandswijziging;
DROP TABLE IF EXISTS commitinfo;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS selectie;
