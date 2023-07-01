CREATE TABLE IF NOT EXISTS bestandswijziging_zoekterm_regelnummer
(
    id  BIGSERIAL PRIMARY KEY,
    idbestandswijzigingzoekterm bigint NOT NULL,
    regelnummer integer,
    regelsoort character varying NOT null check (regelsoort in ('oud', 'nieuw')),
    CONSTRAINT bestandswijzigingzoekterm_fk FOREIGN KEY (idbestandswijzigingzoekterm)
        REFERENCES bestandswijziging_zoekterm(id) ON DELETE CASCADE
)
TABLESPACE pg_default;



ALTER TABLE IF EXISTS bestandswijziging_zoekterm_regelnummer
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging_zoekterm_regelnummer TO appl;
GRANT USAGE ON SEQUENCE bestandswijziging_zoekterm_regelnummer_id_seq TO appl;

COMMENT ON TABLE bestandswijziging_zoekterm_regelnummer
    IS 'regelnummer in een difftext waar enen zoekterm is gevonden';

-- indexen
CREATE INDEX bestandswijziging_zoekterm_regelnummer_idbestandswijzigingzoekterm_idx ON bestandswijziging_zoekterm_regelnummer (idbestandswijzigingzoekterm);



