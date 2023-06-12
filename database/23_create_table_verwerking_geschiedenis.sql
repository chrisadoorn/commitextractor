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
)
TABLESPACE pg_default;

-- wij voegen in het proces uitsluitend records toe.
GRANT INSERT, SELECT ON TABLE verwerking_geschiedenis TO appl;
GRANT USAGE ON SEQUENCE verwerking_geschiedenis_id_seq TO appl;


COMMENT ON TABLE verwerking_geschiedenis
    IS 'Tabel om de uitgevoerde processtappen bij te houden van de verwerking.';