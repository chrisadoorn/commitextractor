CREATE TABLE IF NOT EXISTS selectie
(
    id BIGSERIAL PRIMARY KEY,
    selectionmoment date NOT NULL,
    language varchar,
    commitsminimum integer,
    contributorsminimum integer,
    excludeforks boolean,
    onlyforks boolean,
    hasissues boolean,
    haspulls boolean,
    haswiki boolean,
    haslicense boolean,
    committedmin date,
    locatie varchar default 'https://github.com/'
)

TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE selectie TO appl;
GRANT USAGE ON SEQUENCE selectie_id_seq TO appl;

COMMENT ON TABLE selectie
    IS 'Wanneer de projecten selectie is uitgevoerd, en met welke criteria';