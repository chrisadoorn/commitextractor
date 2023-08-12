
CREATE TABLE IF NOT EXISTS auteur_tellingen
(
    auteur    integer NOT NULL,
    project   character varying not null,
    projectid integer not null,
    aantal_kandidaat  integer default 0,
    aantal_bevestigd integer default 0,
    aantal_totaal integer default 0,
    aantal_ns_kandidaat  integer default 0,
    aantal_ns_bevestigd integer default 0,
    aantal_ns_totaal integer default 0,
    CONSTRAINT auteur_tellingen_uk UNIQUE (auteur, projectid)
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE auteur_tellingen TO appl;

COMMENT ON TABLE auteur_tellingen
    IS 'hulptabel om resultaten te sommeren. Aantal_kandidaat: bestandswijziging_zoekterm. aantal_bevestigd: aantal kandidaten die na parsen bevestigd zijn
        aantal_ns_kandidaat: aantal bestandswijziging_zoekterm met uitsluiting van suspicious commits, aantal_ns_bevestigd: aantal bevestigd na uitsluiting van suspicious commits'
    ;

