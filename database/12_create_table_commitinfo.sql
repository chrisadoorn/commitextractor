CREATE TABLE IF NOT EXISTS commitinfo
(
    id BIGSERIAL PRIMARY KEY,
    idproject bigint NOT NULL,
    commitdatumtijd date NOT NULL,
    hashvalue varchar NOT NULL,
    username varchar NOT NULL,
    emailaddress varchar NOT NULL,
    author_id integer,
    remark text,
    CONSTRAINT commitinfo_fk FOREIGN KEY (idproject)
        REFERENCES project(id) ON DELETE CASCADE
)

TABLESPACE pg_default;

CREATE INDEX commitinfo_idproject_idx ON commitinfo USING btree (idproject);
CREATE INDEX commitinfo_idauthor_idx ON commitinfo USING btree (author_id);

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE commitinfo TO appl;
GRANT USAGE ON SEQUENCE commitinfo_id_seq TO appl;

