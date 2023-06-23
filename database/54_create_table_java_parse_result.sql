CREATE TABLE IF NOT EXISTS java_parse_result
(
    id bigint NOT NULL PRIMARY KEY,
    zoekterm varchar NOT NULL,
    bw_id bigint NOT NULL,
    commit_id bigint NOT NULL,
    is_gebruik bool,
    is_nieuw bool,
    is_verwijderd bool,
    bevat_unknown bool,
    usage_list_achteraf varchar NULL,
    usage_list_vooraf  varchar NULL
)

TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE java_parse_result TO appl;

