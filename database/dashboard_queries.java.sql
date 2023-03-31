SELECT v.naam, v.einde_extractie - v.start_extractie as tijdsduur, p.project_size, v.status, v.resultaat, v.start_extractie, v.einde_extractie, v.processor
	FROM test.verwerk_project v
	join test.project p on v.id = p.id
	order by p.project_size DESC, start_extractie DESC;
	
select status, resultaat, count(status) as c_status, count(resultaat) as c_resultaat
from test.verwerk_project
group by status, resultaat
order by status;

select * from test.processor;

SELECT max(einde_extractie) - min(start_extractie) as tijdsduur
     , min(start_extractie)as begintijd
	 , max(einde_extractie) as eindtijd
	FROM test.verwerk_project;

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
where naam = 'alfasoftware/morf';
