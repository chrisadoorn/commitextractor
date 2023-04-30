set schema 'test';
-- Table: java_zoekterm

-- DROP TABLE IF EXISTS java_zoekterm;

CREATE TABLE IF NOT EXISTS java_zoekterm
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    zoekterm character varying COLLATE pg_catalog."default" NOT NULL,
    categorie character varying COLLATE pg_catalog."default" NOT NULL,
    "package" character varying COLLATE pg_catalog."default",
    opmerking character varying COLLATE pg_catalog."default",
    CONSTRAINT java_zoekterm_pkey PRIMARY KEY (id),
    CONSTRAINT zoekterm_uk UNIQUE (zoekterm)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS java_zoekterm
    OWNER to postgres;

GRANT SELECT, REFERENCES ON TABLE java_zoekterm TO appl;

GRANT ALL ON TABLE java_zoekterm TO postgres;