CREATE TABLE IF NOT EXISTS bestandswijziging_zoekterm
(
    id  BIGSERIAL PRIMARY KEY,
    idbestandswijziging bigint NOT NULL,
    zoekterm character varying NOT NULL,
    falsepositive boolean DEFAULT false,
    regelnummers integer[],
    aantalgevonden integer DEFAULT 0,
    CONSTRAINT bestandswijziging_fk FOREIGN KEY (idbestandswijziging)
        REFERENCES bestandswijziging(id) ON DELETE CASCADE
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging_zoekterm TO appl;
GRANT USAGE ON SEQUENCE bestandswijziging_zoekterm_id_seq TO appl;

COMMENT ON TABLE bestandswijziging_zoekterm
    IS 'analyse info over voorkomen van een zoekterm in een bestandswijziging';

-- indexen
-- CREATE INDEX bestandswijziging_zoekterm_zoekterm_idx ON bestandswijziging_zoekterm (zoekterm);
