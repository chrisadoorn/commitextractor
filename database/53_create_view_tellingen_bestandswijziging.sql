-- View: test.tellingen_bestandswijziging

-- DROP VIEW test.tellingen_bestandswijziging;

CREATE OR REPLACE VIEW test.tellingen_bestandswijziging
 AS
 SELECT b.id,
    ( SELECT a.resultaattelling
           FROM test."analyse" a
          WHERE a.idbestandswijziging = b.id AND a.idanalysemethode = (( SELECT m.id
                   FROM test.methode m
                  WHERE m.zoekwijze::text = 'telling diff regel'::text AND m.zoekterm::text = '+'::text))) AS aantal_nieuwe_regels,
    ( SELECT a.resultaattelling
           FROM test."analyse" a
          WHERE a.idbestandswijziging = b.id AND a.idanalysemethode = (( SELECT m.id
                   FROM test.methode m
                  WHERE m.zoekwijze::text = 'telling diff regel'::text AND m.zoekterm::text = '-'::text))) AS aantal_oude_regels
   FROM test.bestandswijziging b;

ALTER TABLE test.tellingen_bestandswijziging
    OWNER TO postgres;

GRANT SELECT ON TABLE test.tellingen_bestandswijziging TO appl;
GRANT ALL ON TABLE test.tellingen_bestandswijziging TO postgres;

