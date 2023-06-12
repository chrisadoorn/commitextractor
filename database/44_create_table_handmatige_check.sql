CREATE TABLE IF NOT EXISTS handmatige_check
(
    id BIGSERIAL PRIMARY KEY,
    projectnaam character varying NOT NULL,
    project_id bigint NOT NULL,
    bwz_id bigint NOT NULL,
    zoekterm character varying NOT NULL,
    falsepositive boolean NOT NULL,
    regelnummers integer[],
    bestandswijziging_id bigint NOT NULL,
    commit_datum date NOT NULL,
    commit_sha character varying NOT NULL,
    commit_remark character varying NULL,
    gecontroleerd boolean DEFAULT FALSE,
    akkoord boolean NULL,
    opmerking character varying NULL,
    CONSTRAINT bestandswijziging_fk FOREIGN KEY (bestandswijziging_id)
        REFERENCES bestandswijziging(id) ON DELETE CASCADE
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE handmatige_check TO appl;
GRANT USAGE ON SEQUENCE handmatige_check_id_seq TO appl;

--indexen
CREATE INDEX handmatige_check_idbestandswijziging_idx ON handmatige_check (bestandswijziging_id);
CREATE INDEX handmatige_check_zoekterm_idx ON handmatige_check (zoekterm);
CREATE INDEX handmatige_check_project_idx ON handmatige_check (project_id);
CREATE INDEX handmatige_check_bwz_idx ON handmatige_check (bwz_id);
