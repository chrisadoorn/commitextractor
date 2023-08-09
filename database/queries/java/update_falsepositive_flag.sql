
select count(*) from java_parse_result;				 -- 159115
select count(*) from java_parser_selection_view jpsv;-- 159468
select count(*) from bestandswijziging_zoekterm;	 -- 426487
select count(*) from bestandswijziging_zoekterm
where  falsepositive = false ;                      -- 159468 Zou gelijk moeten zijn aan jpsv count
select count(*) from java_parser_selection_view sv 
where sv.id not in (select id from java_parse_result);  -- 353 (= 159468 - 159115 ) = uitval tijdens parse step = 2.2% 
select count(*) from wijziging_lineage wl ;     -- 2512590
select count(*) from bestandswijziging b ;


-- reset false positive flag voor parse stap
update bestandswijziging_zoekterm
set afkeurreden = null 
   ,falsepositive = false 
where afkeurreden  is not null;  

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

-- update gebruik libraries
update bestandswijziging_zoekterm 
set falsepositive = true 
   ,afkeurreden = 'onjuist_gebruik_libraries'
where id in(select id
			from java_parse_result 
			where zoekterm in (select zoekterm
							   from java_zoekterm jz 
							   where categorie = 'libraries')
			and is_in_namespace = false) ;


-- reset uitgesloten reden
update bestandswijziging 
set uitgesloten = false 
   ,uitsluitreden = null
where uitgesloten = true;


-- update bestandswijziging, zet uitsluiting
update bestandswijziging 
set uitgesloten = true 
   ,uitsluitreden = 'parse_exception'
where id in (select distinct(idbestandswijziging)
			from bestandswijziging_zoekterm bz 
			where falsepositive = true 
			and afkeurreden = 'parse_exception');   

update bestandswijziging 
set uitgesloten = true 
   ,uitsluitreden = 'parse_error'
where id in (select distinct(idbestandswijziging)
			from bestandswijziging_zoekterm bz 
			where falsepositive = true 
			and afkeurreden = 'parse_error')
and uitgesloten = false;   

select uitsluitreden, count(uitsluitreden) as aantal
from bestandswijziging b 
where uitgesloten = true
group by uitsluitreden;







