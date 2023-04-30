set schema 'test';

-- Table: zoekterm

DROP TABLE IF EXISTS zoekterm;

CREATE TABLE IF NOT EXISTS zoekterm
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    extensie character varying NOT NULL,
    zoekwoord character varying NOT NULL,
    CONSTRAINT zoekterm_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS zoekterm
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE zoekterm TO appl;

GRANT ALL ON TABLE zoekterm TO postgres;

COMMENT ON TABLE zoekterm
    IS 'basale zoektermen';

ALTER TABLE IF EXISTS zoekterm
    ADD CONSTRAINT uc_zoekwoord UNIQUE (zoekwoord, extensie);

COMMENT ON CONSTRAINT uc_zoekwoord ON zoekterm
    IS 'zoekwoorden moeten uniek zijn';