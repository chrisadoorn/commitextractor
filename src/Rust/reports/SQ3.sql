--SQ.3 How has the usage of multi-core programming primitives changed over time? Is there a trend?

--SQL statements voor het beantwoorden van SQ3

--view per jaar met de zoektermen-tellingen
 SET SCHEMA 'test';
CREATE OR REPLACE VIEW bestandswijziging_zoekterm_jaar
AS SELECT
    cast(date_part('year',commitdatumtijd) as int) as jaarveld, count(bz.id) as telling
	from test.bestandswijziging_zoekterm bz,
		 test.bestandswijziging b,
		 test.commitinfo ci
	where b.idcommit = ci.id
		  and bz.idbestandswijziging = b.id
		  and bz.falsepositive = 'False'
    group by jaarveld;

-- Permissions
GRANT SELECT ON TABLE bestandswijziging_zoekterm_jaar TO appl;

--maken tabel met wijzigingen per jaar


CREATE TABLE IF NOT EXISTS compare_jaar
( jaar int not null
 ,count_all_file_changes int
 ,count_mc_file_changes int
 ,avg_mc_commit decimal
 ,CONSTRAINT compare_jaar_pkey PRIMARY KEY(jaar)
 )
TABLESPACE pg_default;

grant select on compare_jaar to appl;

-- herbeginnen
truncate table compare_jaar;

-- vul tabel met totalen
insert into compare_jaar( jaar, count_all_file_changes)
select cast(date_part('year',commitdatumtijd) as int) as jaarveld, count(b.id)
from commitinfo c,
     bestandswijziging b
where c.id = b.idcommit
group by jaarveld
order by jaarveld asc;

-- update tabel met totalen voor multi-core commits
UPDATE compare_jaar AS cj
SET count_mc_file_changes = sub.count_value
from (
	select jaarveld, telling as count_value
	from bestandswijziging_zoekterm_jaar
) AS sub
where cj.jaar = sub.jaarveld;

-- update tabel met gemiddelde per jaar
update compare_jaar
set avg_mc_commit = (cast(count_mc_file_changes as dec)  / cast(count_all_file_changes as dec)) * 100 ;

