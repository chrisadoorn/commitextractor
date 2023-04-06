set schema 'test';

-- Table: analysis

DROP TABLE IF EXISTS analysis;

CREATE TABLE IF NOT EXISTS analysis
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idproject bigint NOT NULL,
    idcommit bigint NOT NULL,
    idbestand bigint NOT NULL,
    username varchar COLLATE pg_catalog."default" NOT NULL,
    emailaddress varchar COLLATE pg_catalog."default" NOT NULL,
    keyword text COLLATE pg_catalog."default" NOT NULL,
    loc integer
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS analysis
    OWNER to postgres;
   
ALTER TABLE analysis ADD CONSTRAINT analysis_fk1 FOREIGN KEY (idcommit) REFERENCES commitinfo(id) ON DELETE CASCADE;
ALTER TABLE analysis ADD CONSTRAINT analysis_fk2 FOREIGN KEY (idproject) REFERENCES project(id) ON DELETE CASCADE;
ALTER TABLE analysis ADD CONSTRAINT analysis_fk3 FOREIGN KEY (idbestand) REFERENCES bestandswijziging(id) ON DELETE CASCADE;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE analysis TO appl;

GRANT ALL ON TABLE analysis TO postgres;