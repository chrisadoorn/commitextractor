-- Table: test.verwerk_project

DROP TABLE IF EXISTS test.verwerk_project;

CREATE TABLE IF NOT EXISTS test.verwerk_project
(
    id bigint NOT NULL ,
    naam "char" NOT NULL,
    datum_extractie date NOT NULL DEFAULT (now())::date,
    processor "char",
    status "char" NOT NULL DEFAULT 'nieuw',
    resultaat "char",

    CONSTRAINT verwerk_project_pkey PRIMARY KEY (id),
    CONSTRAINT project_fkey FOREIGN KEY (id)
        REFERENCES test.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS test.verwerk_project
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE test.verwerk_project TO appl;

GRANT ALL ON TABLE test.verwerk_project TO postgres;
-- Index: fki_selectie_fkey

-- DROP INDEX IF EXISTS test.fki_selectie_fkey;