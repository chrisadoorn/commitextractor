set schema 'test';

-- Table: commitinfo

DROP TABLE IF EXISTS commitinfo;

CREATE TABLE IF NOT EXISTS commitinfo
(
    idcommit bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idproject bigint NOT NULL,
    commitdatumtijd date NOT NULL,
    hashvalue varchar COLLATE pg_catalog."default" NOT NULL,
    username varchar COLLATE pg_catalog."default" NOT NULL,
    emailaddress varchar COLLATE pg_catalog."default" NOT NULL,
    remark text COLLATE pg_catalog."default",
    CONSTRAINT commit_pkey PRIMARY KEY (idcommit)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS commitinfo
    OWNER to postgres;
   
ALTER TABLE commitinfo ADD CONSTRAINT commitinfo_fk FOREIGN KEY (idproject) REFERENCES test.project(id) ON DELETE CASCADE;


GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE commitinfo TO appl;

GRANT ALL ON TABLE commitinfo TO postgres;