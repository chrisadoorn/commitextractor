set schema 'test';

-- Table: processor

DROP TABLE IF EXISTS processor;

CREATE TABLE IF NOT EXISTS processor
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    identifier character (36) NOT NULL,
    start_processing timestamp without time zone DEFAULT now(),
    einde_processing timestamp without time zone,
    status character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'actief'::character varying,
    CONSTRAINT processor_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS processor
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE processor TO appl;

GRANT ALL ON TABLE processor TO postgres;

COMMENT ON TABLE processor
    IS 'Tabel om de status bij te houden van de verwerkende processen. Status mag zijn: actief, gestopt, geblokt.';
