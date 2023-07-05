CREATE TABLE IF NOT EXISTS bestandswijziging_zoekterm
(
    id  BIGSERIAL PRIMARY KEY,
    idbestandswijziging bigint NOT NULL,
    zoekterm character varying NOT NULL,
    falsepositive boolean DEFAULT false,
    afkeurreden character varying NULL,
    aantalgevonden_oud integer DEFAULT 0,
    aantalgevonden_nieuw integer DEFAULT 0,
    CONSTRAINT bestandswijziging_fk FOREIGN KEY (idbestandswijziging)
        REFERENCES bestandswijziging(id) ON DELETE cascade,
    CONSTRAINT bestandswijziging_ak unique (idbestandswijziging, zoekterm)
)
TABLESPACE pg_default;



ALTER TABLE IF EXISTS bestandswijziging_zoekterm
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging_zoekterm TO appl;
GRANT USAGE ON SEQUENCE bestandswijziging_zoekterm_id_seq TO appl;

COMMENT ON TABLE bestandswijziging_zoekterm
    IS 'Analyse info over voorkomen van een zoekterm in een bestandswijziging. Wordt gevuld met potentiele hits. False positive kan op true gezet worden als ontdekt is er een reden gevonden is waarom dat niet zo is. Optioneel kan dan afkeurreden gevuld worden. Aantalgevonden_oud bevat aantal gevonden keyword voorkomens in oude regels. aantalgevonden_nieuw in nieuwe regels.';

-- indexen
CREATE INDEX bestandswijziging_zoekterm_idbestandswijziging_idx ON bestandswijziging_zoekterm (idbestandswijziging);
CREATE INDEX bestandswijziging_zoekterm_zoekterm_idx ON bestandswijziging_zoekterm (zoekterm);
CREATE INDEX bestandswijziging_zoekterm_ak_idx ON bestandswijziging_zoekterm (idbestandswijziging, zoekterm);

