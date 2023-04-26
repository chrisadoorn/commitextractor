set schema 'test';

-- Table: bestandswijziging_zoekterm

DROP TABLE IF EXISTS bestandswijziging_zoekterm;

CREATE TABLE IF NOT EXISTS bestandswijziging_zoekterm
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idbestandswijziging bigint NOT NULL,
    zoekterm character varying NOT NULL,
    falsepositive boolean DEFAULT false,
    regelnummers integer[],
    aantalgevonden integer DEFAULT 0,
    CONSTRAINT bestandswijziging_zoekterm_pk PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE bestandswijziging_zoekterm ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (idbestandswijziging) REFERENCES bestandswijziging(id) ON DELETE CASCADE;
CREATE INDEX bestandswijziging_zoekterm_idbestandswijziging_idx ON bestandswijziging_zoekterm (idbestandswijziging);
CREATE INDEX bestandswijziging_zoekterm_zoekterm_idx ON bestandswijziging_zoekterm (zoekterm);


ALTER TABLE IF EXISTS bestandswijziging_zoekterm
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging_zoekterm TO appl;

GRANT ALL ON TABLE bestandswijziging_zoekterm TO postgres;

COMMENT ON TABLE bestandswijziging_zoekterm
    IS 'analyse info over voorkomen van een zoekterm in een bestandswijziging';

