CREATE TABLE IF NOT EXISTS java_parse_result
(
    id bigint NOT NULL PRIMARY KEY,
    zoekterm varchar NOT NULL,
    bw_id bigint NOT NULL,
    commit_id bigint NOT NULL,
    is_in_namespace bool,
    is_gebruik_gewijzigd bool,
    is_nieuw bool,
    is_verwijderd bool,
    vooraf_usage_ontbreekt bool,
    achteraf_nieuw_usage bool,
    bevat_unknown bool,
    parse_error_vooraf bool,
    parse_error_achteraf bool,
    len_usage_vooraf int default 0,
    len_usage_achteraf int default 0,
    usage_list_achteraf varchar NULL,
    usage_list_vooraf  varchar NULL
)

TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE java_parse_result TO appl;

