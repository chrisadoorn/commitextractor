select count(*) from java_parse_result jpr;              -- totaal : 132622
select count(distinct bw_id) from java_parse_result jpr; -- totaal :  84872

-- uitsluiten van gevallen waar een parse error optrad: 
--  vergelijking voor en achteraf levert onbetrouwbare resultaten
select count(*) from java_parse_result jpr 
where parse_error_vooraf is true or parse_error_achteraf = true; -- 349 afgekeurd (0.2%)

-- uitsluiten van gevallen waar tekstachteraf leeg is. ( bestand verwijderd, multi-core statement wijziging is incidenteel)
select count(distinct bw_id) from java_parse_result jpr -- 10020 (11.8 %)
where is_verwijderd = true ;
-- verhoudingsgewijs meer verwijderd? 
select count(*) from bestandswijziging b  -- 2072141 totaal
where tekstachteraf  is null; -- verwijderd 248234 (12.0%)

-- uitsluiten van gevallen waar het zoekwoord in een andere namespace stond
select count(*) from java_parse_result jpr  
where is_in_namespace = false;             -- 14005 afgekeurd, want het betreft een ander zoekwoord. ( Condition, Flow komen  )
-- En waar ging dit dan om?
select zoekterm, count(zoekterm) as aantal_gebruik  -- 68 zoektermen. Condition, Lock, Executor, Future, Flow, ConcurrentHashMap
from java_parse_result jpr                          -- project_geen_bestandswijziging_wel_verwerkt_202307102055.txt
where is_in_namespace = false
group by zoekterm 
order by aantal_gebruik DESC; 
-- TODO Controleren, waarom ConcurrentHashMap 1070 x is uitgesloten, maar 3483 niet. 
-- is_in_namespace controle moet aangepast worden. 
-- controle op zowel tekst_vooraf als tekstachteraf
-- is_waar als minstens 1 van 2 klopt. 
select is_in_namespace, count(is_in_namespace) as aantal
from java_parse_result jpr
where zoekterm = 'AtomicLong'
group by is_in_namespace;
  
select b.id, b.tekstachteraf, b.tekstvooraf , b.difftext  
from bestandswijziging b 
where b.id in (
select bw_id  
from java_parse_result jpr
where zoekterm = 'AtomicLong'
and is_in_namespace = false)
limit 10;

-- verhoudingsgewijs meer nieuwe? 
select count(*) from bestandswijziging b  -- 2072141 totaal
where tekstvooraf is null; -- nieuw 461654 (22.3%)

select count(distinct bw_id) from java_parse_result jpr 
where is_nieuw = true;  -- nieuw: 33494 (39.5% van 84872)

select count( distinct bw_id) from java_parse_result jpr  -- nieuw: 29635 op 51792 ( 57.2% )
where  parse_error_vooraf is false 
and    parse_error_achteraf = false
and    is_verwijderd = false
and    is_in_namespace = true 
and  ( vooraf_usage_ontbreekt = true
       or achteraf_nieuw_usage = true )
and is_nieuw = true;

-- omkering: hoe zit het met de verwijderingen? 
select count(*) from bestandswijziging b  -- 2072141 totaal
where tekstachteraf  is null; -- verwijderd 248234 (12.0%)

select count(distinct bw_id) from java_parse_result jpr 
where is_verwijderd = true;  -- verwijderd: 10020 (11.8% van 84872)

select count( distinct bw_id) from java_parse_result jpr  -- verwijderd: 9014 op 60810 ( 14.8% )
where  parse_error_vooraf is false 
and    parse_error_achteraf = false
and    is_in_namespace = true 
and  ( vooraf_usage_ontbreekt = true
       or achteraf_nieuw_usage = true )
and    is_verwijderd = true

