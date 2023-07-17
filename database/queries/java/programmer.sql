
select count(*) from java_parse_result;				 -- 132622
select count(*) from java_parser_selection_view jpsv -- 133117
select count(*) from bestandswijziging_zoekterm;	 -- 351302
select count(*) from bestandswijziging_zoekterm
where  falsepositive = false ;                      -- 133117 Zou gelijk moeten zijn aan jpr count
select count(*) from java_parser_selection_view sv 
where sv.id not in (select id from java_parse_result);  -- 495 (= 133117 - 132622 ) = uitval tijdens parse step = 3.7% 
select count(*) from wijziging_lineage wl ;     -- 2210694


-- opnieuw uitvoeren van uitgevallen parse step
update verwerk_project 
set processtap = 'zoekterm_controleren'
   ,resultaat = 'verwerkt'
   ,processor = null
   ,status = 'gereed'
where processtap = 'java_parsing'
-- and id != 60803
and id in (select distinct(wl.projectid)
from java_parser_selection_view jpr
    ,wijziging_lineage wl 
where wl.bestandswijzingzoekterm_id = jpr.id );



select wl.* 
from wijziging_lineage wl
    ,bestandswijziging_zoekterm bz 
where bz.id = wl.bestandswijzingzoekterm_id
and  bz.falsepositive = false 
and bz.id not in (select id from java_parse_result)


select count(bz.id)
from java_parse_result jpr
    ,bestandswijziging_zoekterm bz 
where bz.id  = jpr.id 
and bevat_unknown = true  -- 376 klopt
and is_in_namespace = true -- 174
and parse_error_vooraf = false 
and parse_error_achteraf = false
and is_verwijderd = false;





