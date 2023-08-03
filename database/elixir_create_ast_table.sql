CREATE TABLE IF NOT EXISTS v11.abstract_syntax_trees (
    id BIGSERIAL PRIMARY KEY,
    bestandswijziging_id BIGINT NOT NULL,
    tekstvooraf text,
    tekstachteraf text,
    difftext text,
    tekstvooraf_ast text,
    tekstachteraf_ast text
)








