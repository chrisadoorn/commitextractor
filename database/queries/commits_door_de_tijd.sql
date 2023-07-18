CREATE TABLE IF NOT EXISTS compare_jaar
( jaar int not null
 ,count_all_commit int
 ,count_mc_commit int
 ,avg_mc_commit decimal
 ,CONSTRAINT compare_jaar_pkey PRIMARY KEY(jaar)
 )
TABLESPACE pg_default;

-- herbeginnen
truncate table compare_jaar;

-- vul tabel met totalen
insert into compare_jaar( jaar, count_all_commit)
select cast(date_part('year',commitdatumtijd) as int) as jaarveld, count(id)
from commitinfo c 
group by jaarveld
order by jaarveld asc;

-- update tabel met totalen voor multi-core commits
update compare_jaar
set count_mc_commit = (select count(id)
					   from commitinfo c 
					   where id in (select distinct commitid
                	   				 from wijziging_lineage wl
                 	   				 where falsepositive = false)
					   and cast(date_part('year',commitdatumtijd) as int) = compare_jaar.jaar);

-- update tabel met gemiddelde per jaar
update compare_jaar
set avg_mc_commit = (cast(count_mc_commit as dec)  / cast(count_all_commit as dec)) * 100 ;

select * from compare_jaar
order by jaar asc;



                 	
