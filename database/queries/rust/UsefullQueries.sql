--bij meerdere keren draaien GhSearch
TRUNCATE test.selectie RESTART IDENTITY cascade;
TRUNCATE test.project RESTART IDENTITY cascade;
TRUNCATE test.verwerk_project RESTART IDENTITY cascade;
TRUNCATE test.verwerking_geschiedenis RESTART IDENTITY cascade;

--opvolging verwerking
select processtap, status, resultaat, count(status) as c_status, count(resultaat) as c_resultaat
from test.verwerk_project
group by processtap, status, resultaat
order by processtap,status;

-- opnieuw uitvoeren van uitgevallen stap
TRUNCATE test.commitinfo RESTART IDENTITY cascade;

update test.verwerk_project
set processtap = 'selectie'
   ,resultaat = 'verwerkt'
   ,processor = null
   ,status = 'gereed'
where processtap = 'extractie';

