CREATE TABLE IF NOT EXISTS bestandswijziging
(
    id BIGSERIAL PRIMARY KEY,
    idcommit bigint NOT NULL,
    filename varchar,
    locatie varchar,
    extensie varchar,
    difftext text NOT NULL,
    tekstvooraf text,
    tekstachteraf text,
    CONSTRAINT bestandswijziging_fk FOREIGN KEY (idcommit)
        REFERENCES commitinfo(id) ON DELETE CASCADE
)

TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging TO appl;
GRANT USAGE ON SEQUENCE bestandswijziging_id_seq TO appl;

-- indexen
CREATE INDEX bestandswijziging_idcommit_idx ON bestandswijziging USING btree (idcommit);
