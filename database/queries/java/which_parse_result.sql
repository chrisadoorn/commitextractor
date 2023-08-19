select count(*) from java_parse_result jpr;              -- totaal : 162050
select count(distinct bw_id) from java_parse_result jpr; -- totaal :  85016

-- uitsluiten van gevallen waar een parse error optrad: 
--  vergelijking voor en achteraf levert onbetrouwbare resultaten
select count(*) from java_parse_result jpr 
where parse_error_vooraf is true or parse_error_achteraf = true; -- 387 afgekeurd (0.2%)

-- uitsluiten van gevallen waar tekstachteraf leeg is. ( bestand verwijderd, multi-core statement wijziging is incidenteel)
select count(distinct bw_id) from java_parse_result jpr -- 10028 (11.8 %)
where is_verwijderd = true ;
-- verhoudingsgewijs meer verwijderd? 
select count(*) from bestandswijziging b  -- 2072141 totaal
where tekstachteraf  is null; -- verwijderd 248234 (12.0%)

-- uitsluiten van gevallen waar het zoekwoord in een andere namespace stond
select count(*) from java_parse_result jpr  
where is_in_namespace = false;             -- 14030 (10.6%) afgekeurd, want het betreft een ander zoekwoord. ( Condition, Flow komen  )
-- En waar ging dit dan om?
select zoekterm, count(zoekterm) as aantal_gebruik  -- 68 zoektermen. Condition, Lock, Executor, Future, Flow, ConcurrentHashMap
from java_parse_result jpr                          -- project_geen_bestandswijziging_wel_verwerkt_202307102055.txt
where is_in_namespace = false
group by zoekterm 
order by aantal_gebruik DESC; 
-- Controleren, waarom ConcurrentHashMap 172 x is uitgesloten, maar 4386 keer niet. 
-- Er blijken echt mensen te zijn die een eigen ConcurrentHashMap aanmaken. (Of variant van. Dit tellen wij niet mee, wel wanner hun versie van ConcurrentHashMap gebruikt wordt.)
-- voorbeeld: import edu.emory.mathcs.backport.java.util.concurrent.ConcurrentHashMap;
select is_in_namespace, count(is_in_namespace) as aantal
from java_parse_result jpr
where zoekterm = 'ConcurrentHashMap'
group by is_in_namespace;
  
select b.id, b.tekstachteraf, b.tekstvooraf , b.difftext  
from bestandswijziging b 
where b.id in (
select bw_id  
from java_parse_result jpr
where zoekterm = 'ConcurrentHashMap'
and is_in_namespace = false)
limit 10;

-- verhoudingsgewijs meer nieuwe? 
select count(*) from bestandswijziging b  -- 2072141 totaal
where tekstvooraf is null; -- nieuw 461654 (22.3%)

select count(distinct bw_id) from java_parse_result jpr 
where is_nieuw = true;  -- nieuw: 33595 (39.5% van 85016)

select count( distinct bw_id) from java_parse_result jpr  -- nieuw: 29635 op 51820 ( 57.2% )
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
where is_verwijderd = true;  -- verwijderd: 10028 (11.8% van 85016)

select count( distinct bw_id) from java_parse_result jpr  -- verwijderd: 9014 op 60834 ( 14.8% )
where  parse_error_vooraf is false 
and    parse_error_achteraf = false
and    is_in_namespace = true 
and  ( vooraf_usage_ontbreekt = true
       or achteraf_nieuw_usage = true )
and    is_verwijderd = true

select * from java_parser_selection_view jpr 
where zoekterm = '@Lock';

select * from java_parse_result jpr 
where zoekterm = 'Collections.synchronizedList'
order by bw_id ASC;

select * from java_parse_result jpr 
where zoekterm in ( select zoekterm 
                    from java_zoekterm jz
                    where categorie = 'libraries');

select count(*) from java_parser_selection_view;
select naam
from project p 
where id = 60803;

