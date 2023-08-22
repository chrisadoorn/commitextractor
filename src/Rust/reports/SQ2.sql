--SQ.2 What is the correlation between multi-core programming primitives and the percentage of programmers using them?

--SQL statements voor het beantwoorden van SQ2
--primitives and counts
select zoekterm, count(idbestandswijziging) as freq
from test.bestandswijziging_zoekterm
where bz.falsepositive = 'False'
group by zoekterm
order by freq desc

--per project # aantal verschillende zoektermen + frequentie ervan
select idproject, b.zoekterm, count(bz.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging_zoekterm b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.idbestandswijziging = b.id
     and bz.falsepositive = 'False'
group by idproject, b.zoekterm
order by idproject asc

--per project en per auteur # aantal verschillende zoektermen + frequentie ervan
select idproject, author_id, b.zoekterm, count(bz.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.idbestandswijziging = b.id
     and bz.falsepositive = 'False'
group by idproject, author_id, b.zoekterm
order by idproject asc