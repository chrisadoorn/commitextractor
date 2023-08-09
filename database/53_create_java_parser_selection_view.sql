
CREATE OR REPLACE VIEW java_parser_selection_view
AS SELECT  bz.id as id, b.id as bw_id, c.id as commit_id, p.id as project_id, bz.zoekterm, b.tekstvooraf, b.tekstachteraf, jz.categorie, jz.packagenaam
from    bestandswijziging b,
        commitinfo c,
        project p,
        bestandswijziging_zoekterm bz,
        java_zoekterm jz 
where   b.idcommit = c.id
and     c.idproject = p.id
and     bz.zoekterm = jz.zoekterm
and     bz.idbestandswijziging = b.id
and     ( bz.falsepositive = false
		 -- omdat de diff analyzer niet om kan gaan als er een punt(.) of een ad (@) teken in het keyword voorkomt 
         -- wordt zolang dit niet is opgelost, hier gefixt door deze or op te nemen. 
         or bz.zoekterm in (select jz.zoekterm 
					from java_zoekterm jz 
					where jz.zoekterm not in (select jpr.zoekterm 
											  	from java_parse_result jpr
					    						  	,bestandswijziging_zoekterm bz 
												where jpr.id = bz.id
												and bz.falsepositive = false
												group by jpr.zoekterm))
        )
order by bw_id;

-- Permissions
GRANT SELECT ON TABLE java_parser_selection_view TO appl;
