--SQ.1 How is the usage of multi-core programming primitives distributed among programmers?

--SQL statements voor het beantwoorden van SQ1

--aantal projecten --> 882 stuks
select count(distinct(idproject))
from test.commitinfo ci

--aantal MC-projecten --> 541 stuks
select count(distinct(idproject))
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.idbestandswijziging = b.id
	  and bz.falsepositive = 'False'

--number of MC-file changes
select count(id)
from test.bestandswijziging_zoekterm
where falsepositive = 'False'

--tellingen tabel SQ1
select count(unieke_mc_auteur), sum(filechanges), sum(mcfilechanges)
from test.sq1_table
--where unieke_mc_auteur = 1
where unieke_auteur > 900000000

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
	  and bz.idbestandswijziging = b.id
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
		  and bz.idbestandswijziging = b.id
		  and bz.falsepositive = 'False'
	group by author_id
) AS sub
where sq1.unieke_auteur = sub.author_id;


--2e extra tabel voor SQ1--programmeurs en hun projecten + aanduiding of zij hier MC hebben geinjecteerd
SET SCHEMA 'test';
CREATE TABLE IF NOT EXISTS auteur_verschillendeProjecten
(
    auteur integer not null,
    idproject integer default 0,
    MCfileproject integer default 0
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE auteur_verschillendeProjecten TO appl;

-- gooi eerst alles weer leeg.
truncate table auteur_verschillendeProjecten;

-- unieke auteurs en projecten waaraan deze hebben meegewerkt
insert into auteur_verschillendeProjecten(auteur, idproject)
select distinct(author_id), idproject
from test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
group by author_id, idproject;

-- vlaggen van projecten als MC als de auteur er een MC aan heeft toegevoegd
update auteur_verschillendeProjecten as sq2
set MCfileproject = 1
from (
	select ci.author_id, ci.idproject
	from test.bestandswijziging_zoekterm bz,
    	 test.bestandswijziging b,
	     test.commitinfo ci
	where b.idcommit = ci.id
	  and bz.idbestandswijziging = b.id
	  and bz.falsepositive = 'False'
) as sub
where sq2.auteur = sub.author_id
  and sq2.idproject = sub.idproject

--514 auteurs hebben in verschillende projecten gewerkt (4337 niet in meerdere, dus count <2)
select count(distinct(auteur))
from test.auteur_verschillendeProjecten
where auteur in (select subq.auteur
				from test.auteur_verschillendeProjecten subq
				group by  subq.auteur
				having count(distinct subq.idproject) > 1
				order by subq.auteur desc)

-- 230 multi-project auteurs hebben hebben in minstens 1 project mc geprogrameerd, 1156 MC-programmeurs slechts in 1 project (dus bij count <2)
select count(distinct(auteur))
from test.auteur_verschillendeProjecten
where mcfileproject = 1
  and auteur in (select subq.auteur
				from test.auteur_verschillendeProjecten subq
				group by  subq.auteur
				having count(distinct subq.idproject) > 1
				order by subq.auteur desc)

--MC auteurs en hun projecten
select auteur, idproject, mcfileproject
from test.auteur_verschillendeProjecten
where auteur in (select subq.auteur
				from test.auteur_verschillendeProjecten subq
				where mcfileproject = 1)
order by auteur, idproject

-- 63 auteurs hebben in meer dan 1 project mc gedaan
select distinct(auteur), count(idproject) as freq
from test.auteur_verschillendeProjecten
where mcfileproject = 1
group by auteur
order by freq desc
