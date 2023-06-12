CREATE TABLE IF NOT EXISTS project
(
    id BIGSERIAL PRIMARY KEY,
    naam varchar NOT NULL,
    idselectie bigint NOT NULL,
    main_language varchar,
    is_fork boolean,
    license varchar,
    forks integer,
    contributors integer,
    project_size bigint,
    create_date date,
    last_commit date,
    number_of_languages integer,
    aantal_commits integer,
    languages text,
    CONSTRAINT selectie_fkey FOREIGN KEY (idselectie)
        REFERENCES selectie (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE project TO appl;
GRANT USAGE ON SEQUENCE project_id_seq TO appl;

-- Index: fki_selectie_fkey
CREATE INDEX IF NOT EXISTS fki_selectie_fkey
    ON project USING btree
    (idselectie ASC NULLS LAST)
    TABLESPACE pg_default;