set schema 'test';

-- Table: verwerking_geschiedenis

DROP TABLE IF EXISTS verwerking_geschiedenis;

CREATE TABLE IF NOT EXISTS verwerking_geschiedenis
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    project_id bigint NOT NULL,
    project_naam character varying COLLATE pg_catalog."default" NOT NULL,
    start_verwerking timestamp without time zone,
    einde_verwerking timestamp without time zone,
    processor character(36) COLLATE pg_catalog."default",
    status character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'nieuw'::character varying,
    resultaat character varying COLLATE pg_catalog."default",
    processtap character varying COLLATE pg_catalog."default",
    CONSTRAINT verwerking_geschiedenis_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS verwerking_geschiedenis
    OWNER to postgres;
   
-- wij voegen in het proces uitsluitend records toe.
GRANT INSERT, SELECT ON TABLE verwerking_geschiedenis TO appl;

GRANT ALL ON TABLE verwerking_geschiedenis TO postgres;

COMMENT ON TABLE verwerking_geschiedenis
    IS 'Tabel om de yuitgevoerde processtappen bij te houden van de verwerking.';