SELECT v.naam, v.processtap,  v.einde_verwerking - v.start_verwerking  as tijdsduur, p.project_size, v.status, v.resultaat, v.start_verwerking , v.einde_verwerking , v.processor
	FROM test.verwerk_project v
	
	join test.project p on v.id = p.id
--	where v.einde_verwerking is not null
	order by p.project_size DESC, start_verwerking DESC;

select v.status, v.resultaat, v.processtap 
, count(v.status), count(v.resultaat), count(v.processtap)
from verwerk_project v
-- where v.einde_extractie is not null
group by v.status, v.resultaat, v.processtap 

UPDATE processor
SET  status='geblokt'
WHERE status='actief';



-- kijk hoever de verwerking van een bepaalde processtap is. 	
select processtap, status, resultaat, count(status) as c_status, count(resultaat) as c_resultaat
from verwerk_project
group by processtap, status, resultaat
order by processtap, status;

select * from test.processor;

-- hoelang heeft een bepaalde stap geduurd? 
SELECT max(einde_verwerking) - min(start_verwerking) as tijdsduur
     , min(start_verwerking)as begintijd
	 , max(einde_verwerking) as eindtijd
	FROM verwerk_project
where processtap = 'zoekterm_vinden';

select count(1) from test.commit;
select count(1) from test.bestandswijziging;

--update test.verwerk_project
--set processor = null   ,start_extractie = null   ,einde_extractie = null   ,resultaat = null   ,status = 'nieuw';
   
--delete from test.processor;   
select count(id) 
from commitinfo c 
where author_id is null;


-- update test.verwerk_project
-- set processor = null   ,start_extractie = null   ,einde_extractie = null   ,resultaat = null   ,status = 'nieuw'
-- where naam = 'googleapis/java-bigtable-hbase';

update test.verwerk_project set status = 'geblokt'
where status = 'nieuw';
update test.verwerk_project set status = 'nieuw'
where naam = 'adyen/adyen-java-api-library';

select count(*) from bestandswijziging_zoekterm bz ; -- 351302
select count(*) from bestandswijziging_zoekterm bz 
where falsepositive = false ; -- 133117



select 
p.id, p.naam, count(c.idproject) as commit_aantal
from commitinfo c 
    ,project p 
where c.idproject = p.id
group by p.id, p.naam, c.idproject
order by commit_aantal asc  

update verwerk_project 
set resultaat = 'geblokt'
where resultaat = 'verwerkt'
and id != 184823;
update verwerk_project
set processtap = 'extractie'
   ,resultaat = 'verwerkt'
where id = 184823;

-- opnieuw uitvoeren van uitgevallen stap
update verwerk_project 
set processtap = 'zoekterm_controleren'
   ,resultaat = 'verwerkt'
   ,processor = null
   ,status = 'gereed'
where processtap = 'java_parsing'
and resultaat = 'mislukt';

update verwerk_project 
set processtap = 'extractie'
   ,resultaat = 'verwerkt'
where id in (184852, 184840, 184844);   

--opnieuw uitvoeren van parsen
update verwerk_project 
set processtap = 'zoekterm_controleren'
   ,resultaat = 'verwerkt'
   ,processor = null
   ,status = 'gereed'
where processtap = 'java_parsing'
and resultaat = 'verwerkt';



-- blok iedere verdere verwerking
update processor 
set status = 'geblokt';

-- gooi autor info weer leeg voor herstest
update commitinfo 
set author_id = null 
where idproject in (184852, 184840, 184844);   


select count(*) 
from bestandswijziging_zoekterm bz   -- 53049
where falsepositive = false          -- 16928
and afkeurreden is not null;         --  9256

select 
c.id, count(b.idcommit) as bestandswijzing_aantal
from commitinfo c 
    ,bestandswijziging b 
where b.idcommit = c.id
group by c.id, b.idcommit
order by bestandswijzing_aantal desc

select 
p.id, p.naam, 
( select   count(c.idproject) as commit_aantal
   from    commitinfo c 
  where    c.idproject = p.id
  group by c.idproject)
from project p
order by commit_aantal asc;

-- aantal commits en bestandswijzigingen per project
select 
p.id, p.naam, 
( select   count(c.idproject) as commit_aantal
   from    commitinfo c 
  where    c.idproject = p.id
  group by c.idproject),
(select count(b.idcommit) as bestandswijzing_aantal
 from bestandswijziging b 
 where b.idcommit in (select c.id
                      from commitinfo c 
                      where c.idproject = p.id)
)
from project p
where p.id in ( select distinct(c1.idproject) from commitinfo c1)
order by bestandswijzing_aantal asc;

select 
b.id,
(select a.resultaattelling
	from "analyse" a 
	where a.idbestandswijziging	= b.id
	and a.idanalysemethode = (
		select m.id 
		from methode m
		where zoekwijze = 'telling diff regel'
		and zoekterm = '+')) as aantal_nieuwe_regels,
(select a.resultaattelling
	from "analyse" a 
	where a.idbestandswijziging	= b.id
	and a.idanalysemethode = (
		select m.id 
		from methode m
		where zoekwijze = 'telling diff regel'
		and zoekterm = '-')) as aantal_oude_regels		
from bestandswijziging b

-- aantal bestanden met gevonden zoektermen per project
select p.naam, count(p.naam) as aantal
from bestandswijziging_zoekterm bz,
     bestandswijziging b,
     commitinfo c,
     project p 
where bz.idbestandswijziging = b.id
and   b.idcommit = c.id 
and   c.idproject = p.id 
group by p.naam
order by 2 DESC;   


-- zet testdata in 

insert into bestandswijziging_zoekterm (idbestandswijziging, zoekterm)
select b.id, 'synchronized' from bestandswijziging b;


-- select text van bestandswijziging
select 
bz.zoekterm, bz.falsepositive , bz.regelnummers, 
b.difftext, b.tekstachteraf  
from bestandswijziging_zoekterm bz 
    ,bestandswijziging b
    ,commitinfo c
    ,project p 
where bz.idbestandswijziging = b.id
and   b.idcommit = c.id
and   c.idproject = p.id 
and   p.naam = 'dockstore/dockstore'
limit 1;

-- kijk wat er handmatig gecontroleerd is. 
select distinct(project_id), projectnaam 
from handmatige_check hc 
order by project_id

select count(*) 
from prod.handmatige_check 
where gecontroleerd = true;

insert into bestandswijziging_zoekterm_regelnummer (idbestandswijziging, zoekterm, regelnummer, regelsoort)
values ( 104939, 'Callable', unnest (ARRAY[12,13,3]), 'oud')


-- verwijder bestandswijzigingen, commitinfo van mislukte projecten voor opnieuw proberen
select id, naam from project
where id in (select id from verwerk_project vp where resultaat = 'mislukt');

delete from bestandswijziging 
where idcommit in (
select id from commitinfo c 
where idproject in (select id from verwerk_project vp where resultaat = 'mislukt'));


delete from commitinfo c 
where idproject in (select id from verwerk_project vp where resultaat = 'mislukt');


-- wat is afgekeurd, en waarom
select afkeurreden, falsepositive, count(afkeurreden) as aantal_afkeurreden, count(falsepositive)  
from bestandswijziging_zoekterm bz 
group by afkeurreden, falsepositive
order by 3, 4;


-- welke bestandswijzigingen zijn afgekeurd vanwege parse fouten?
select distinct(idbestandswijziging)
from bestandswijziging_zoekterm bz 
where falsepositive = true 
and afkeurreden in ('parse_exception', 'parse_error'); -- 2646

-- andere afkeurredenen voor deze bestandswijzigingen
select *
from bestandswijziging_zoekterm bz 
where (falsepositive = false 
       or afkeurreden not in ('parse_exception', 'parse_error'))
and bz.idbestandswijziging in ( select distinct(bz2.idbestandswijziging)
								from bestandswijziging_zoekterm bz2 
								where bz2.falsepositive = true 
								and bz2.afkeurreden in ('parse_exception', 'parse_error')); 
							
select difftext,  tekstvooraf , tekstachteraf  
from bestandswijziging b 
where b.id = 1030290;


select *
from java_parse_result jpr 
 where jpr.usage_list_achteraf like '%identifier%';
-- where jpr.bw_id = 64541;

							
