set schema 'test';

-- Table: bestandswijziging_info

DROP TABLE IF EXISTS bestandswijziging_info;

CREATE TABLE IF NOT EXISTS bestandswijziging_info
(
    id bigint NOT NULL,
    regels_oud integer default 0,
    regels_nieuw integer default 0,
    CONSTRAINT bestandswijziging_info_pk PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE bestandswijziging_info ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (id) REFERENCES bestandswijziging(id) ON DELETE CASCADE;


ALTER TABLE IF EXISTS bestandswijziging_info
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging_info TO appl;

GRANT ALL ON TABLE bestandswijziging_info TO postgres;

COMMENT ON TABLE bestandswijziging_info
    IS 'analyse info over een bestandswijziging';

