-- Table: test.methode

-- DROP TABLE IF EXISTS test.methode;

CREATE TABLE IF NOT EXISTS test.methode
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    zoekterm character varying COLLATE pg_catalog."default" NOT NULL,
    zoekwijze character varying COLLATE pg_catalog."default" NOT NULL,
    resultaattype character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT analyse_methode_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS test.methode
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE test.methode TO appl;

GRANT ALL ON TABLE test.methode TO postgres;

COMMENT ON TABLE test.methode
    IS 'zoekterm: keyword waarnaar gezocht word
zoekwijze: manier waarop gezocht wordt, voorbeelden: ''tel voorkomens'', ''eerste woord hiervoor'', ''komt voor''
resulttaattype: welk type resultaat er uit een methode komt: integer ( telling), boolean, een woord of regel, dan varchar ';