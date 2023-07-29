
select count(*) from java_parse_result;				 -- 159115
select count(*) from java_parser_selection_view jpsv;-- 159468
select count(*) from bestandswijziging_zoekterm;	 -- 426487
select count(*) from bestandswijziging_zoekterm
where  falsepositive = false ;                      -- 159468 Zou gelijk moeten zijn aan jpsv count
select count(*) from java_parser_selection_view sv 
where sv.id not in (select id from java_parse_result);  -- 353 (= 159468 - 159115 ) = uitval tijdens parse step = 2.2% 
select count(*) from wijziging_lineage wl ;     -- 2512590
select count(*) from bestandswijziging b ;


-- parse exceptions 353
update bestandswijziging_zoekterm 
set falsepositive = true 
   ,afkeurreden = 'parse_exception'
where id in (select id 
             from java_parser_selection_view 
             where id not in (select id 
                              from java_parse_result))            
and falsepositive = false;

-- parse erors --315
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
			 and is_in_namespace = true )            
and falsepositive = false;


-- verwijderd uitsluiten   --22215
select count(*) from java_parse_result jpr 
where is_verwijderd = true;

update bestandswijziging_zoekterm 
set falsepositive = true 
   ,afkeurreden = 'verwijderd'
where id in (select id 
             from java_parse_result
             where is_verwijderd = true)            
and falsepositive = false;


            
            
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
			 and   is_in_namespace = false)            
and falsepositive = false;


-- verhoudingsgewijs meer verwijderd? 
select count(*) from bestandswijziging b  -- 2072141 totaal
-- uitsluiten van gevallen waar het zoekwoord in een andere namespace stond

-- reset false positive flag voor parse stap
update bestandswijziging_zoekterm
set afkeurreden = null 
   ,falsepositive = false 
where afkeurreden  is not null;  
