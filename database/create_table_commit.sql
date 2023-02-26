set schema 'test';

-- Table: commit

-- DROP TABLE IF EXISTS commit;

CREATE TABLE IF NOT EXISTS commit
(
    idcommit bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    idproject bigint NOT NULL,
    commitdatumtijd date NOT NULL,
    hashvalue character(40) COLLATE pg_catalog."default" NOT NULL,
    username character(255) COLLATE pg_catalog."default" NOT NULL,
    emailaddress character(255) COLLATE pg_catalog."default" NOT NULL,
    remark text COLLATE pg_catalog."default",
    CONSTRAINT commit_pkey PRIMARY KEY (idcommit)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS commit
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE commit TO appl;

GRANT ALL ON TABLE commit TO postgres;