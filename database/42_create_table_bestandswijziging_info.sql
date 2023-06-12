CREATE TABLE IF NOT EXISTS bestandswijziging_info
(
    id bigint NOT NULL,
    regels_oud integer default 0,
    regels_nieuw integer default 0,
    CONSTRAINT bestandswijziging_info_pk PRIMARY KEY (id),
    CONSTRAINT bestandswijziging_fk FOREIGN KEY (id)
        REFERENCES bestandswijziging(id) ON DELETE CASCADE
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging_info TO appl;


COMMENT ON TABLE bestandswijziging_info
    IS 'analyse info over een bestandswijziging. Id is gelijk aan de id van de bestandswijziging';

