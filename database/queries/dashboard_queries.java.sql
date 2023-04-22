SELECT v.naam, v.einde_extractie - v.start_extractie as tijdsduur, p.project_size, v.status, v.resultaat, v.start_extractie, v.einde_extractie, v.processor
	FROM test.verwerk_project v
	
	join test.project p on v.id = p.id
	where v.einde_extractie is not null
	order by p.project_size DESC, start_extractie DESC;

select v.status, v.resultaat
, count(v.status), count(v.resultaat)
from verwerk_project v
-- where v.einde_extractie is not null
group by v.status, v.resultaat

UPDATE processor
SET  status='geblokt'
WHERE status='';



	
select status, resultaat, count(status) as c_status, count(resultaat) as c_resultaat
from test.verwerk_project
group by status, resultaat
order by status;

select * from test.processor;

SELECT max(einde_extractie) - min(start_extractie) as tijdsduur
     , min(start_extractie)as begintijd
	 , max(einde_extractie) as eindtijd
	FROM prod.verwerk_project
where einde_extractie > '2023-04-05 17:59:00';

select count(1) from test.commit;
select count(1) from test.bestandswijziging;

--update test.verwerk_project
--set processor = null   ,start_extractie = null   ,einde_extractie = null   ,resultaat = null   ,status = 'nieuw';
   
--delete from test.processor;   
	

-- update test.verwerk_project
-- set processor = null   ,start_extractie = null   ,einde_extractie = null   ,resultaat = null   ,status = 'nieuw'
-- where naam = 'googleapis/java-bigtable-hbase';

update test.verwerk_project set status = 'geblokt'
where status = 'nieuw';
update test.verwerk_project set status = 'nieuw'
where naam = 'adyen/adyen-java-api-library';


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
order by commit_aantal asc;

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


-- zet testdata in 

insert into bestandswijziging_zoekterm (idbestandswijziging, zoekterm)
select b.id, 'synchronized' from bestandswijziging b;