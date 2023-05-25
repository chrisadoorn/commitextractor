set schema 'test';

-- Table: handmatige_check

DROP TABLE IF EXISTS handmatige_check;

CREATE TABLE IF NOT EXISTS handmatige_check
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
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
    CONSTRAINT handmatige_check_pk PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE handmatige_check ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (bestandswijziging_id) REFERENCES bestandswijziging(id) ON DELETE CASCADE;
CREATE INDEX handmatige_check_idbestandswijziging_idx ON handmatige_check (bestandswijziging_id);
CREATE INDEX handmatige_check_zoekterm_idx ON handmatige_check (zoekterm);
CREATE INDEX handmatige_check_project_idx ON handmatige_check (project_id);
CREATE INDEX handmatige_check_bwz_idx ON handmatige_check (bwz_id);


ALTER TABLE IF EXISTS handmatige_check
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE handmatige_check TO appl;

GRANT ALL ON TABLE handmatige_check TO postgres;

INSERT INTO handmatige_check (projectnaam,
    project_id,
    bwz_id,
    zoekterm,
    falsepositive,
    regelnummers,
    bestandswijziging_id,
    commit_datum,
    commit_sha,
    commit_remark)
select  p.naam, p.id,  bz.id, bz.zoekterm, bz.falsepositive, bz.regelnummers, bz.idbestandswijziging, c.commitdatumtijd, c.hashvalue, c.remark
from prod.bestandswijziging_zoekterm bz, prod.bestandswijziging b, prod.commitinfo c, prod.project p
where  bz.idbestandswijziging = b.id
and b.idcommit = c.id and c.idproject = p.id
order by p.id, c.commitdatumtijd, c.hashvalue ;

