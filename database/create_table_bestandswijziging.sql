-- Table: test.bestandswijziging

-- DROP TABLE IF EXISTS test.bestandswijziging;

CREATE TABLE IF NOT EXISTS test.bestandswijziging
(
    idbestandswijziging bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idcommit bigint NOT NULL,
    filename character varying(512) COLLATE pg_catalog."default",
    locatie character varying(512) COLLATE pg_catalog."default",
    extensie character varying(20) COLLATE pg_catalog."default",
    difftext text COLLATE pg_catalog."default" NOT NULL,
    tekstvooraf text COLLATE pg_catalog."default",
    tekstachteraf text COLLATE pg_catalog."default",
    CONSTRAINT bestandswijziging_pkey PRIMARY KEY (idbestandswijziging)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS test.bestandswijziging
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE test.bestandswijziging TO appl;

GRANT ALL ON TABLE test.bestandswijziging TO postgres;