CREATE TABLE IF NOT EXISTS zoekterm
(
    id BIGSERIAL PRIMARY KEY,
    extensie character varying NOT NULL,
    zoekwoord character varying NOT NULL,
    CONSTRAINT uc_zoekwoord UNIQUE (zoekwoord, extensie)
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE zoekterm TO appl;
GRANT USAGE ON SEQUENCE zoekterm_id_seq TO appl;

COMMENT ON TABLE zoekterm
    IS 'basale zoektermen';

COMMENT ON CONSTRAINT uc_zoekwoord ON zoekterm
    IS 'zoekwoorden moeten uniek zijn';