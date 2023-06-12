CREATE TABLE IF NOT EXISTS processor
(
    id BIGSERIAL PRIMARY KEY,
    identifier character (36) NOT NULL,
    start_processing timestamp without time zone DEFAULT now(),
    einde_processing timestamp without time zone,
    status varchar NOT NULL DEFAULT 'actief',
    CONSTRAINT processor_un UNIQUE (identifier)
)
TABLESPACE pg_default;


GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE processor TO appl;
GRANT USAGE ON SEQUENCE processor_id_seq TO appl;


COMMENT ON TABLE processor
    IS 'Tabel om de status bij te houden van de verwerkende processen. Status mag zijn: actief, gestopt, geblokt.';
