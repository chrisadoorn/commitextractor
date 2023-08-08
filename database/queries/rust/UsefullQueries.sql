--tabel (en andere tabellen eraan gelieerd) leegmaken en herstarten id
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

-- tellen gebruik zoekterm
select count(b.id)
from test.bestandswijziging b
where b.extensie = '.rs'
  and b.difftext like '%use runtime-tokio%'

-- opzoeken difftext na vinden zoekterm
select bz.idbestandswijziging, b.difftext
from test.bestandswijziging_zoekterm bz,
	 test.bestandswijziging b
where bz.idbestandswijziging = b.id
	 and bz.idbestandswijziging = '553'

--opzoeken projectid,naam & commitid na vinden zoekterm
select c.idproject, d.naam, c.id
from test.bestandswijziging_zoekterm bz,
	 test.bestandswijziging b,
	 test.commitinfo c,
	 test.project d
where bz.idbestandswijziging = b.id
	 and bz.idbestandswijziging = '839'
	 and b.idcommit = c.id
	 and c.idproject = d.id