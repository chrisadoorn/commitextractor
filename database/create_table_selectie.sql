-- Table: test.selectie

-- DROP TABLE IF EXISTS test.selectie;

CREATE TABLE IF NOT EXISTS test.selectie
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

ALTER TABLE IF EXISTS test.selectie
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE test.selectie TO appl;

GRANT ALL ON TABLE test.selectie TO postgres;

COMMENT ON TABLE test.selectie
    IS 'Wanneer de projecten selectie is uitgevoerd, en met welke criteria';