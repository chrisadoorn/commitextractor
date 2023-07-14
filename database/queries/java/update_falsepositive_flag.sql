
select count(*) from java_parse_result;				 -- 132815
select count(*) from java_parser_selection_view jpsv -- 133117
select count(*) from bestandswijziging_zoekterm;	 -- 351302
select count(*) from bestandswijziging_zoekterm
where  falsepositive = false ;                      -- 133117 Zou gelijk moeten zijn aan jpr count
select count(*) from java_parser_selection_view sv 
where sv.id not in (select id from java_parse_result);  -- 302 (= 133117 - 132815 ) = uitval tijdens parse step = 2.2% 
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

-- parse exceptions
update bestandswijziging_zoekterm 
set falsepositive = true 
   ,afkeurreden = 'parse_exception'
where id in (select id 
             from java_parser_selection_view 
             where id not in (select id 
                              from java_parse_result));


-- verwijderd uitsluiten   --17311
select count(*) from java_parse_result jpr 
where is_verwijderd = true;

update bestandswijziging_zoekterm 
set falsepositive = true 
   ,afkeurreden = 'verwijderd'
where id in (select id 
             from java_parse_result
             where is_verwijderd = true);

            
-- niet in namespace uitsluiten --12975
select count(*) from java_parse_result jpr 
where is_verwijderd = false 
and   is_in_namespace = false;

update bestandswijziging_zoekterm 
set falsepositive = true 
   ,afkeurreden = 'andere_namespace'
where id in (select id 
             from java_parse_result
             where is_verwijderd = false 
			 and   is_in_namespace = false);


-- parse erors --280
select count(*) 
from java_parse_result
where (parse_error_vooraf = true 
       or parse_error_achteraf = true)
and is_verwijderd = false 
and is_in_namespace = true;

			
update bestandswijziging_zoekterm 
set falsepositive = true 
   ,afkeurreden = 'parse_error'
where id in (select id 
             from java_parse_result
             where (parse_error_vooraf = true 
                    or parse_error_achteraf = true)
             and is_verwijderd = false 
			 and is_in_namespace = true );


-- verhoudingsgewijs meer verwijderd? 
select count(*) from bestandswijziging b  -- 2072141 totaal
-- uitsluiten van gevallen waar het zoekwoord in een andere namespace stond

select count (distinct author_id)
from commitinfo c ;
