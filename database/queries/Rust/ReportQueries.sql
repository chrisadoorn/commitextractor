--SQ.1 How is the usage of multi-core programming primitives distributed among programmers?
--SQ.2 What is the correlation between multi-core programming primitives and the percentage of programmers using them?
--SQ.3 How has the usage of multi-core programming primitives changed over time? Is there a trend?

--unieke projecten met MC primitieven
select count(distinct(idproject))
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging_zoekterm b,
	 test.commitinfo ci
where bz.idbestandswijziging = b.id
     and b.id = ci.id

select distinct(idproject)
from test.commitinfo ci

--per project # aantal verschillende zoektermen + frequentie ervan
select idproject, b.zoekterm, count(bz.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging_zoekterm b,
	 test.commitinfo ci
where bz.idbestandswijziging = b.id
     and b.id = ci.id
group by idproject, b.zoekterm
order by idproject asc

--per project en per auteur # aantal verschillende zoektermen + frequentie ervan
select idproject, author_id, b.zoekterm, count(bz.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging_zoekterm b,
	 test.commitinfo ci
where bz.idbestandswijziging = b.id
     and b.id = ci.id
group by idproject, author_id, b.zoekterm
order by idproject asc