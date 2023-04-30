-- Deze file bevat de SQL statements om de database te initialiseren
-- De statements zijn in de juiste volgorde geplaatst
-- Er moet al een schema aanwezig zijn, de naam kan met set schema worden aangepast
set schema 'test_sample';

-- Tabellen
--10
CREATE TABLE IF NOT EXISTS selectie
(
    id BIGSERIAL PRIMARY KEY,
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
    committedmin date
);


--11
CREATE TABLE IF NOT EXISTS project
(
    id BIGSERIAL PRIMARY KEY,
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
    CONSTRAINT selectie_fkey FOREIGN KEY (idselectie)
        REFERENCES selectie (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE INDEX IF NOT EXISTS fki_selectie_fkey
    ON project USING btree
        (idselectie ASC NULLS LAST)
    TABLESPACE pg_default;

--12
CREATE TABLE IF NOT EXISTS commitinfo
(
    id BIGSERIAL PRIMARY KEY,
    idproject bigint NOT NULL,
    commitdatumtijd date NOT NULL,
    hashvalue varchar COLLATE pg_catalog."default" NOT NULL,
    username varchar COLLATE pg_catalog."default" NOT NULL,
    emailaddress varchar COLLATE pg_catalog."default" NOT NULL,
    author_id integer,
    remark text COLLATE pg_catalog."default"
);

ALTER TABLE commitinfo ADD CONSTRAINT commitinfo_fk FOREIGN KEY (idproject) REFERENCES project(id) ON DELETE CASCADE;
CREATE INDEX commitinfo_idproject_idx ON commitinfo USING btree (idproject);
CREATE INDEX commitinfo_idauthor_idx ON commitinfo USING btree (author_id);

--13
CREATE TABLE IF NOT EXISTS bestandswijziging
(
    id BIGSERIAL PRIMARY KEY,
    idcommit bigint NOT NULL,
    filename character varying(512) COLLATE pg_catalog."default",
    locatie character varying(512) COLLATE pg_catalog."default",
    extensie character varying(20) COLLATE pg_catalog."default",
    difftext text COLLATE pg_catalog."default" NOT NULL,
    tekstachteraf text COLLATE pg_catalog."default"
);

ALTER TABLE bestandswijziging ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (idcommit) REFERENCES commitinfo(id) ON DELETE CASCADE;
CREATE INDEX bestandswijziging_idcommit_idx ON bestandswijziging USING btree (idcommit);

--21
CREATE TABLE IF NOT EXISTS processor
(
    id BIGSERIAL PRIMARY KEY,
    identifier character (36) NOT NULL,
    start_processing timestamp without time zone DEFAULT now(),
    einde_processing timestamp without time zone,
    status character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'actief'::character varying,
    CONSTRAINT processor_un UNIQUE (identifier)
);

--22

CREATE TABLE IF NOT EXISTS verwerk_project
(
    id BIGSERIAL PRIMARY KEY,
    naam character varying COLLATE pg_catalog."default" NOT NULL,
    start_verwerking timestamp without time zone,
    einde_verwerking timestamp without time zone,
    processor character(36) COLLATE pg_catalog."default",
    status character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'nieuw'::character varying,
    resultaat character varying COLLATE pg_catalog."default",
    processtap character varying COLLATE pg_catalog."default",
    CONSTRAINT project_fkey FOREIGN KEY (id)
        REFERENCES project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

ALTER TABLE verwerk_project ADD CONSTRAINT verwerk_project_fk FOREIGN KEY (processor) REFERENCES processor(identifier);

--23
CREATE TABLE IF NOT EXISTS verwerking_geschiedenis
(
    id BIGSERIAL PRIMARY KEY,
    project_id bigint NOT NULL,
    project_naam character varying COLLATE pg_catalog."default" NOT NULL,
    start_verwerking timestamp without time zone,
    einde_verwerking timestamp without time zone,
    processor character(36) COLLATE pg_catalog."default",
    status character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'nieuw'::character varying,
    resultaat character varying COLLATE pg_catalog."default",
    processtap character varying COLLATE pg_catalog."default"
);


--41
CREATE TABLE IF NOT EXISTS zoekterm
(
    id BIGSERIAL PRIMARY KEY,
    extensie character varying NOT NULL,
    zoekwoord character varying NOT NULL
);

--42
CREATE TABLE IF NOT EXISTS bestandswijziging_info
(
    id BIGSERIAL PRIMARY KEY,
    regels_oud integer default 0,
    regels_nieuw integer default 0
);

ALTER TABLE bestandswijziging_info ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (id) REFERENCES bestandswijziging(id) ON DELETE CASCADE;

--43
CREATE TABLE IF NOT EXISTS bestandswijziging_zoekterm
(
    id BIGSERIAL PRIMARY KEY,
    idbestandswijziging bigint NOT NULL,
    zoekterm character varying NOT NULL,
    falsepositive boolean DEFAULT false,
    regelnummers integer[],
    aantalgevonden integer DEFAULT 0
);


ALTER TABLE bestandswijziging_zoekterm ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (idbestandswijziging) REFERENCES bestandswijziging(id) ON DELETE CASCADE;
CREATE INDEX bestandswijziging_zoekterm_idbestandswijziging_idx ON bestandswijziging_zoekterm (idbestandswijziging);
CREATE INDEX bestandswijziging_zoekterm_zoekterm_idx ON bestandswijziging_zoekterm (zoekterm);



-- procedures
--31

CREATE OR REPLACE PROCEDURE registreer_processor(
    IN p_identifier character,
    INOUT p_new_id bigint)
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    insert into processor ("identifier")
    values (p_identifier)
    RETURNING "id" INTO p_new_id;
    return;
END;
$BODY$;

--32
CREATE OR REPLACE PROCEDURE deregistreer_processor(
    IN p_identifier character)
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    update processor
    set status = 'gestopt'
      ,einde_processing = now()
    where identifier = p_identifier;
    return;
END;
$BODY$;

--33

CREATE OR REPLACE PROCEDURE registreer_verwerking(
    IN p_projectid bigint,
    IN p_resultaat character varying)
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    update verwerk_project
    set einde_verwerking = now()
      ,status = 'gereed'
      ,resultaat = p_resultaat
      ,processor = null
    where id = p_projectid;
END;
$BODY$;


--34
CREATE OR REPLACE PROCEDURE verwerk_volgend_project(
    IN p_identifier character,
    IN p_vorige_stap character varying,
    IN p_nieuwe_stap character varying,
    INOUT p_new_id bigint,
    INOUT p_projectnaam character varying,
    INOUT p_rowcount integer)
    LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    v_processor bigint;
BEGIN
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
      and processtap = p_vorige_stap
      and status = 'verwerkt'
    LIMIT 1 ;

    if not found then
-- er is niets meer te verwerken.
        select 0 into p_rowcount;
        return;
    end if;

-- update record op basis van eerder gevonden id.
    update verwerk_project
    set start_verwerking = now()
      ,einde_verwerking = null
      ,processor = p_identifier
      ,status = 'bezig'
      ,processtap = p_nieuwe_stap
    where processor is null
      and processtap = p_vorige_stap
      and status = 'verwerkt'
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
