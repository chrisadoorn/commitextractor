set schema 'test';

-- Table: selectie

CREATE TABLE IF NOT EXISTS selectie
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    selectionmoment date NOT NULL,
    language character varying COLLATE pg_catalog."default",
    commitsminimum integer,
    contributorsminimum integer,
    excludeforks boolean,
    onlyforks boolean,
    hasissues boolean,
    haspulls boolean,
    haswiki boolean,
    haslicense boolean,
    committedmin date,
    CONSTRAINT selectie_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS selectie
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE selectie TO appl;

GRANT ALL ON TABLE selectie TO postgres;

COMMENT ON TABLE selectie
    IS 'Wanneer de projecten selectie is uitgevoerd, en met welke criteria';

-- Table: project

CREATE TABLE IF NOT EXISTS project
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    naam character varying COLLATE pg_catalog."default" NOT NULL,
    idselectie bigint NOT NULL,
    main_language character varying COLLATE pg_catalog."default",
    is_fork boolean,
    license character varying COLLATE pg_catalog."default",
    forks integer,
    contributors integer,
    project_size bigint,
    create_date date,
    last_commit date,
    number_of_languages integer,
    aantal_commits integer,
    languages text COLLATE pg_catalog."default",
    CONSTRAINT project_pkey PRIMARY KEY (id),
    CONSTRAINT selectie_fkey FOREIGN KEY (idselectie)
        REFERENCES selectie (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS project
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE project TO appl;

GRANT ALL ON TABLE project TO postgres;
-- Index: fki_selectie_fkey

-- DROP INDEX IF EXISTS fki_selectie_fkey;

CREATE INDEX IF NOT EXISTS fki_selectie_fkey
    ON project USING btree
    (idselectie ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: processor

CREATE TABLE IF NOT EXISTS processor
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    identifier character (36) NOT NULL,
    start_processing timestamp without time zone DEFAULT now(),
    einde_processing timestamp without time zone,
    status character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'actief'::character varying,
    CONSTRAINT processor_pkey PRIMARY KEY (id),
    CONSTRAINT processor_un UNIQUE (identifier)

)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS processor
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE processor TO appl;

GRANT ALL ON TABLE processor TO postgres;

COMMENT ON TABLE processor
    IS 'Tabel om de status bij te houden van de verwerkende processen. Status mag zijn: actief, gestopt, geblokt.';

-- Table: verwerk_project

CREATE TABLE IF NOT EXISTS verwerk_project
(
    id bigint NOT NULL,
    naam character varying COLLATE pg_catalog."default" NOT NULL,
    start_extractie timestamp without time zone,
    einde_extractie timestamp without time zone,
    processor character(36) COLLATE pg_catalog."default",
    status character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'nieuw'::character varying,
    resultaat character varying COLLATE pg_catalog."default",
    CONSTRAINT verwerk_project_pkey PRIMARY KEY (id),
    CONSTRAINT project_fkey FOREIGN KEY (id)
        REFERENCES project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS verwerk_project
    OWNER to postgres;

ALTER TABLE verwerk_project ADD CONSTRAINT verwerk_project_fk FOREIGN KEY (processor) REFERENCES processor(identifier);


GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE verwerk_project TO appl;

GRANT ALL ON TABLE verwerk_project TO postgres;

COMMENT ON TABLE verwerk_project
    IS 'Tabel om de status bij te houden van de verwerking. Status mag zijn: nieuw, gereed, bezig, geblokt. resultaat mag zijn <leeg>, gelukt, mislukt';

-- Table: commitinfo

CREATE TABLE IF NOT EXISTS commitinfo
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idproject bigint NOT NULL,
    commitdatumtijd date NOT NULL,
    hashvalue varchar COLLATE pg_catalog."default" NOT NULL,
    username varchar COLLATE pg_catalog."default" NOT NULL,
    emailaddress varchar COLLATE pg_catalog."default" NOT NULL,
    author_id integer,
    remark text COLLATE pg_catalog."default",
    CONSTRAINT commit_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS commitinfo
    OWNER to postgres;

ALTER TABLE commitinfo ADD CONSTRAINT commitinfo_fk FOREIGN KEY (idproject) REFERENCES project(id) ON DELETE CASCADE;


GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE commitinfo TO appl;

GRANT ALL ON TABLE commitinfo TO postgres;

-- Table: bestandswijziging

CREATE TABLE IF NOT EXISTS bestandswijziging
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idcommit bigint NOT NULL,
    filename character varying(512) COLLATE pg_catalog."default",
    locatie character varying(512) COLLATE pg_catalog."default",
    extensie character varying(20) COLLATE pg_catalog."default",
    difftext text COLLATE pg_catalog."default" NOT NULL,
    tekstachteraf text COLLATE pg_catalog."default",
    CONSTRAINT bestandswijziging_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS bestandswijziging
    OWNER to postgres;

ALTER TABLE bestandswijziging ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (idcommit) REFERENCES commitinfo(id) ON DELETE CASCADE;


GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging TO appl;

GRANT ALL ON TABLE bestandswijziging TO postgres;

-- Table: zoekterm

CREATE TABLE IF NOT EXISTS zoekterm
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    zoekwoord character varying NOT NULL,
    CONSTRAINT zoekterm_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS zoekterm
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE zoekterm TO appl;

GRANT ALL ON TABLE zoekterm TO postgres;

COMMENT ON TABLE zoekterm
    IS 'basale zoektermen';

ALTER TABLE IF EXISTS zoekterm
    ADD CONSTRAINT uc_zoekwoord UNIQUE (zoekwoord);

COMMENT ON CONSTRAINT uc_zoekwoord ON zoekterm
    IS 'zoekwoorden moeten uniek zijn';

-- Table: bestandswijziging_info

CREATE TABLE IF NOT EXISTS bestandswijziging_info
(
    id bigint NOT NULL,
    regels_oud integer default 0,
    regels_nieuw integer default 0,
    CONSTRAINT bestandswijziging_info_pk PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE bestandswijziging_info ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (id) REFERENCES bestandswijziging(id) ON DELETE CASCADE;


ALTER TABLE IF EXISTS bestandswijziging_info
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging_info TO appl;

GRANT ALL ON TABLE bestandswijziging_info TO postgres;

COMMENT ON TABLE bestandswijziging_info
    IS 'analyse info over een bestandswijziging';

-- Table: bestandswijziging_zoekterm

CREATE TABLE IF NOT EXISTS bestandswijziging_zoekterm
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idbestandswijziging bigint NOT NULL,
    zoekterm character varying NOT NULL,
    falsepositive boolean DEFAULT false,
    regelnummers integer[],
    aantalgevonden integer DEFAULT 0,
    CONSTRAINT bestandswijziging_zoekterm_pk PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE bestandswijziging_zoekterm ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (idbestandswijziging) REFERENCES bestandswijziging(id) ON DELETE CASCADE;


ALTER TABLE IF EXISTS bestandswijziging_zoekterm
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging_zoekterm TO appl;

GRANT ALL ON TABLE bestandswijziging_zoekterm TO postgres;

COMMENT ON TABLE bestandswijziging_zoekterm
    IS 'analyse info over voorkomen van een zoekterm in een bestandswijziging';

-- PROCEDURE: registreer_processor(character, bigint)

-- DROP PROCEDURE IF EXISTS registreer_processor(character, bigint);

CREATE OR REPLACE PROCEDURE registreer_processor(
	IN p_identifier character,
	INOUT p_new_id bigint)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN

set schema 'test';
insert into processor ("identifier")
values (p_identifier)
RETURNING "id" INTO p_new_id;

return;

END;
$BODY$;
ALTER PROCEDURE registreer_processor(character, bigint)
    OWNER TO appl;

-- PROCEDURE: registreer_verwerking(bigint, character varying)

-- DROP PROCEDURE IF EXISTS registreer_verwerking(bigint, character varying);

CREATE OR REPLACE PROCEDURE registreer_verwerking(
	IN p_projectid bigint,
	IN p_resultaat character varying)
LANGUAGE 'plpgsql'
AS $BODY$

BEGIN

set schema 'test';

update verwerk_project
set einde_extractie = now()
   ,status = 'gereed'
   ,resultaat = p_resultaat
where id = p_projectid;

END;
$BODY$;
ALTER PROCEDURE registreer_verwerking(bigint, character varying)
    OWNER TO appl;

-- PROCEDURE: verwerk_volgend_project(character, bigint, character varying, integer)
-- DROP PROCEDURE IF EXISTS verwerk_volgend_project(character, bigint, character varying, integer);

CREATE OR REPLACE PROCEDURE verwerk_volgend_project(
	IN p_identifier character,
	INOUT p_new_id bigint,
	INOUT p_projectnaam character varying,
	INOUT p_rowcount integer)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
	v_processor bigint;
BEGIN

set schema 'test';

-- controleer of de processor nog mag doorwerken
SELECT id INTO v_processor
FROM processor
where identifier = p_identifier
and status = 'actief';
if not found then
    select 0 into p_rowcount;
	return;
end if;

-- select id en naam van maximaal 1 record
select id, naam, 0 INTO p_new_id, p_projectnaam, p_rowcount
from verwerk_project
where processor is null
and status = 'nieuw'
LIMIT 1 ;

if not found then
-- er is niets meer te verwerken.
    select 0 into p_rowcount;
	return;
end if;

-- update record op basis van eerder gevonden id.
update verwerk_project
set start_extractie = now()
   ,processor = p_identifier
   ,status = 'bezig'
where processor is null
and status = 'nieuw'
and id =  p_new_id;

-- update de rowcount van default 0 naar aantal geupdate rijen.
-- als dit 0 is, dan is de update mislukt, en was een andere processor eerder.
if not found then
	select 0 into p_rowcount;
else
	select 1 into p_rowcount;
end if;



return;

END;
$BODY$;
ALTER PROCEDURE verwerk_volgend_project(character, bigint, character varying, integer)
    OWNER TO appl;