CREATE TABLE IF NOT EXISTS verwerk_project
(
    id bigint NOT NULL,
    naam varchar NOT NULL,
    locatie varchar NOT NULL DEFAULT 'https://github.com/',
    start_verwerking timestamp without time zone,
    einde_verwerking timestamp without time zone,
    processor character(36),
    status varchar NOT NULL DEFAULT 'nieuw',
    resultaat varchar,
    processtap varchar,
    CONSTRAINT verwerk_project_pkey PRIMARY KEY (id),
    CONSTRAINT project_fkey FOREIGN KEY (id)
        REFERENCES project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT verwerk_project_fk FOREIGN KEY (processor)
        REFERENCES processor(identifier)
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE verwerk_project TO appl;


COMMENT ON TABLE verwerk_project
    IS 'Tabel om de status bij te houden van de verwerking. Status mag zijn: nieuw, gereed, bezig, geblokt. resultaat mag zijn <leeg>, gelukt, mislukt';