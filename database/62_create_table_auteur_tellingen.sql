
CREATE TABLE IF NOT EXISTS auteur_tellingen
(
    auteur    integer NOT NULL,
    project   character varying not null,
    projectid integer not null,
    aantal_kandidaat  integer default 0,
    aantal_bevestigd integer default 0,
    aantal_totaal integer default 0,
    CONSTRAINT auteur_tellingen_uk UNIQUE (auteur, projectid)
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE auteur_tellingen TO appl;

COMMENT ON TABLE auteur_tellingen
    IS 'hulptabel om resultaten te sommeren';

