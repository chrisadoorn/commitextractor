--SQ.1 How is the usage of multi-core programming primitives distributed among programmers?

--SQL statements voor het beantwoorden van SQ1

--aantal projecten --> 882 stuks
select distinct(idproject)
from test.commitinfo ci

--aantal MC-projecten --> 209 stuks
select count(distinct(idproject))
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.id = b.id
	  and bz.falsepositive = 'False'

--number of MC-file changes
select count(id)
from test.bestandswijziging_zoekterm
where falsepositive = 'False'

--primitives and counts
select zoekterm, count(idbestandswijziging) as freq
from test.bestandswijziging_zoekterm
group by zoekterm
order by freq desc

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
     test.bestandswijziging b,
	 test.commitinfo ci
where bz.idbestandswijziging = b.id
     and b.id = ci.id
group by idproject, author_id, b.zoekterm
order by idproject asc

--extra tabel voor SQ1
SET SCHEMA 'test';
CREATE TABLE IF NOT EXISTS SQ1_table
(
    unieke_auteur integer not null,
    unieke_MC_auteur  integer default 0,
    filechanges integer default 0,
    MCfilechanges integer default 0
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE SQ1_table TO appl;

-- gooi eerst alles weer leeg.
truncate table SQ1_table;

-- unieke auteurs en aantal bestandswijzigingen
insert into SQ1_table(unieke_auteur, filechanges)
select distinct(author_id), count(b.id)
from test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
group by author_id;

-- bepalen of het een MC-auteur is
update SQ1_table as sq1
set unieke_MC_auteur = 1
where unieke_auteur in (select ci.author_id
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.id = b.id
	  and bz.falsepositive = 'False');

-- aantal bestandswijzigingen per MC-auteur
UPDATE SQ1_table AS sq1
SET mcfilechanges = sub.count_value
from (
	select author_id, count(bz.id) as count_value
	from test.bestandswijziging_zoekterm bz,
		 test.bestandswijziging b,
		 test.commitinfo ci
	where b.idcommit = ci.id
		  and bz.id = b.id
		  and bz.falsepositive = 'False'
	group by author_id
) AS sub
where sq1.unieke_auteur = sub.author_id;


