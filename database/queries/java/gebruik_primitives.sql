-- zoektermen geordend op mogelijk voorkomen: 113
select zoekterm, count(zoekterm) as aantal 
from java_parse_result jpr 
group by zoekterm
order by aantal desc;

-- zoektermen geordend op actueel voorkomen: 113
select jpr.zoekterm, count(jpr.zoekterm) as aantal 
from java_parse_result jpr
    ,bestandswijziging_zoekterm bz 
where jpr.id = bz.id
and bz.falsepositive = false
group by jpr.zoekterm
order by aantal desc;

-- zoektermen die niet gevonden zijn: 3 stuks: io.reactivex.rxjava2, io.projectreacto en AsyncBoxView.ChildState
select * 
from java_zoekterm jz 
where jz.zoekterm not in (select jpr.zoekterm 
						  	from java_parse_result jpr
    						  	,bestandswijziging_zoekterm bz 
							where jpr.id = bz.id
							group by jpr.zoekterm);

-- zoektermen die niet gevonden zijn, maar wel in de tekstsearch voorkomen: 0 0
select count(zoekterm), zoekterm
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



-- reset de selectie voor zoektermen met punten en @
update bestandswijziging_zoekterm
set afkeurreden = 'niet_afgekeurd',
    falsepositive = false
where zoekterm in ( select zoekterm
                    from java_zoekterm jz
                    where zoekterm like '%.%' or zoekterm like '@%')

