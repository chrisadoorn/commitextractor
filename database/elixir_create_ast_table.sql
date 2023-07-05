CREATE TABLE IF NOT EXISTS abstract_syntax_trees (
    id BIGSERIAL PRIMARY KEY,
    bestandswijziging_id BIGINT NOT NULL,
    tekstvooraf text,
    tekstachteraf text,
    difftext text,
    tekstvooraf_ast text,
    tekstachteraf_ast text,
    CONSTRAINT abstract_syntax_trees_fk FOREIGN KEY (bestandswijziging_id)
        REFERENCES bestandswijziging(id) ON DELETE CASCADE
)








