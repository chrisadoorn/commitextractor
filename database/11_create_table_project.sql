set schema 'test';

-- Table: project

DROP TABLE IF EXISTS project;

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