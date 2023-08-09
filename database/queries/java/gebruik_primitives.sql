-- zoektermen geordend op mogelijk voorkomen: 89
select zoekterm, count(zoekterm) as aantal 
from java_parse_result jpr 
group by zoekterm
order by aantal desc;

-- zoektermen geordend op actueel voorkomen: 89
select jpr.zoekterm, count(jpr.zoekterm) as aantal 
from java_parse_result jpr
    ,bestandswijziging_zoekterm bz 
where jpr.id = bz.id
and bz.falsepositive = false
group by jpr.zoekterm
order by aantal desc;

-- zoektermen die niet gevonden zijn: 27 stuks
select * 
from java_zoekterm jz 
where jz.zoekterm not in (select jpr.zoekterm 
						  	from java_parse_result jpr
    						  	,bestandswijziging_zoekterm bz 
							where jpr.id = bz.id
							and bz.falsepositive = false
							group by jpr.zoekterm);

-- zoektermen die niet gevonden zijn, maar wel in de tekstsearch voorkomen: 24 (2939 entries, 2474 bestandswijzigingen)
select zoekterm 		
from bestandswijziging_zoekterm bz 
where zoekterm in (select jz.zoekterm 
					from java_zoekterm jz 
					where jz.zoekterm not in (select jpr.zoekterm 
											  	from java_parse_result jpr
					    						  	,bestandswijziging_zoekterm bz 
												where jpr.id = bz.id
												and bz.falsepositive = false
												group by jpr.zoekterm))
group by zoekterm ;


-- bestandswijzigingen die hierdoor mogelijk gemist zijn. - 1213
select count(distinct bz.idbestandswijziging) 		
from bestandswijziging_zoekterm bz 
where zoekterm in (select jz.zoekterm 
					from java_zoekterm jz 
					where jz.zoekterm not in (select jpr.zoekterm 
											  	from java_parse_result jpr
					    						  	,bestandswijziging_zoekterm bz 
												where jpr.id = bz.id
												and bz.falsepositive = false
												group by jpr.zoekterm))
and bz.idbestandswijziging not in ( select wl.bestandswijziging 
                                    from wijziging_lineage wl
                                    where falsepositive = false 
                                    and uitgesloten = false )


