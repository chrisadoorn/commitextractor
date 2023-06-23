
CREATE OR REPLACE VIEW java_parser_selection_view
AS SELECT  bz.id as id, b.id as bw_id, c.id as commit_id, p.id as project_id, bz.zoekterm, b.tekstvooraf, b.tekstachteraf
from    bestandswijziging b,
        commitinfo c,
        project p,
        bestandswijziging_zoekterm bz
where   b.idcommit = c.id
and     c.idproject = p.id
and     bz.idbestandswijziging = b.id
and     bz.falsepositive = false
order by bw_id;

-- Permissions
GRANT SELECT ON TABLE java_parser_selection_view TO appl;
