set schema 'test';

-- Table: bestandswijziging

DROP TABLE IF EXISTS bestandswijziging;

CREATE TABLE IF NOT EXISTS bestandswijziging
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idcommit bigint NOT NULL,
    filename character varying(512) COLLATE pg_catalog."default",
    locatie character varying(512) COLLATE pg_catalog."default",
    extensie character varying(20) COLLATE pg_catalog."default",
    difftext text COLLATE pg_catalog."default" NOT NULL,
    tekstachteraf text COLLATE pg_catalog."default",
    CONSTRAINT bestandswijziging_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS bestandswijziging
    OWNER to postgres;
   
ALTER TABLE bestandswijziging ADD CONSTRAINT bestandswijziging_fk FOREIGN KEY (idcommit) REFERENCES commitinfo(id) ON DELETE CASCADE;
CREATE INDEX bestandswijziging_idcommit_idx ON bestandswijziging USING btree (idcommit);


GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE bestandswijziging TO appl;

GRANT ALL ON TABLE bestandswijziging TO postgres;