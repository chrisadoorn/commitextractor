set schema 'test';

-- Table: selectie

DROP TABLE IF EXISTS selectie;

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