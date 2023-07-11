
select count(*) 					-- alle condities: 0
from java_parse_result              -- individueel op 132.622 records = 0.01 %
where bevat_unknown = true          -- 12  was 376 was 461
and is_in_namespace = true          -- 11  
and parse_error_vooraf = false      -- 7
and parse_error_achteraf = false    -- 4

-- hebben we de juiste query? 
select count(*)
from java_parse_result jpr
    ,wijziging_lineage wl 
where wl.zoekterm = jpr.zoekterm 
and  wl.bestandswijziging = jpr.bw_id 
and bevat_unknown = true  -- 376 klopt
and is_in_namespace = true -- 174
and parse_error_vooraf = false 
and parse_error_achteraf = false

-- projecten te replayen:
select distinct(wl.projectid)
from java_parse_result jpr
    ,wijziging_lineage wl 
where wl.zoekterm = jpr.zoekterm 
and  wl.bestandswijziging = jpr.bw_id 
and bevat_unknown = true -- 25 projecten te replayen, na fix 22 
and is_in_namespace = true -- 15 projecten te replayen, na fix
and parse_error_vooraf = false 
and parse_error_achteraf = false

-- welke id's moeten wij fixen?
select wl.bestandswijziging 
from java_parse_result jpr
    ,wijziging_lineage wl 
where wl.zoekterm = jpr.zoekterm 
and  wl.bestandswijziging = jpr.bw_id 
and bevat_unknown = true -- 25 projecten te replayen, na fix
and is_in_namespace = true
and parse_error_vooraf = false 
and parse_error_achteraf = false

-- details opvragen van een unknown
select b.id, jpr.zoekterm, jpr.is_in_namespace, jpr.parse_error_vooraf, jpr.parse_error_achteraf, jpr.usage_list_vooraf, jpr.usage_list_achteraf, b.tekstvooraf, b.tekstachteraf  
from bestandswijziging b 
    , java_parse_result jpr 
where b.id = jpr.bw_id 
and jpr.bevat_unknown = true
and   b.id = 477935
;

-- opnieuw uitvoeren van unknowns
update verwerk_project 
set processtap = 'zoekterm_controleren'
   ,resultaat = 'verwerkt'
   ,processor = null
   ,status = 'gereed'
where processtap = 'java_parsing'
-- and id != 60803
and id in (select distinct(wl.projectid)
from java_parse_result jpr
    ,wijziging_lineage wl 
where wl.zoekterm = jpr.zoekterm 
and  wl.bestandswijziging = jpr.bw_id 
and bevat_unknown = true );


