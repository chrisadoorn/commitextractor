SELECT naam, einde_extractie - start_extractie as tijdsduur, start_extractie, einde_extractie, processor, status, resultaat
	FROM test.verwerk_project
	order by tijdsduur DESC, start_extractie DESC;
	
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
	

