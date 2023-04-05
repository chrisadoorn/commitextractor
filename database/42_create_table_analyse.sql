-- Table: test.analyse

-- DROP TABLE IF EXISTS test.analyse;

CREATE TABLE IF NOT EXISTS test.analyse
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idbestandswijziging bigint NOT NULL,
    idanalysemethode bigint NOT NULL,
    datumtijd date NOT NULL DEFAULT now(),
    resultaatboolean boolean,
    resultaattelling int8range,
    resultaattekst character varying COLLATE pg_catalog."default",
    CONSTRAINT analyse_pkey PRIMARY KEY (idbestandswijziging),
    CONSTRAINT fk_analyse_bestandswijziging FOREIGN KEY (idbestandswijziging)
        REFERENCES test.bestandswijziging (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_analyse_methode FOREIGN KEY (idanalysemethode)
        REFERENCES test.methode (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS test.analyse
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE test.analyse TO appl;

GRANT ALL ON TABLE test.analyse TO postgres;

COMMENT ON TABLE test.analyse
    IS 'Een analyse is het toepassen van een (analyse)methode op een bestandswijziging.
Het moment wordt geregistreerd, en het resultaat van de analyse.
Er wordt 1 resultaat ingevuld, afhankelijk van het resultaattype van de methode. ';
-- Index: fki_fk_analyse_bestandswijziging

-- DROP INDEX IF EXISTS test.fki_fk_analyse_bestandswijziging;

CREATE INDEX IF NOT EXISTS fki_fk_analyse_bestandswijziging
    ON test.analyse USING btree
    (idbestandswijziging ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: fki_fk_analyse_methode

-- DROP INDEX IF EXISTS test.fki_fk_analyse_methode;

CREATE INDEX IF NOT EXISTS fki_fk_analyse_methode
    ON test.analyse USING btree
    (idanalysemethode ASC NULLS LAST)
    TABLESPACE pg_default;