  -- 19 projecten multi core, 26 projecten totaal
  select * from project p 
  where p.id in (select distinct c.idproject 
				   from commitinfo c
				   where c.id in (select distinct commitid
				   				 from wijziging_lineage wl
				   				 where falsepositive = false)
				   and cast(date_part('year',commitdatumtijd) as int) = 2007);

-- welke projecten hebben het grootste aantal wijzigingen in uitschieter 2007? 	
-- openjdk/shenandoah 23.578 meer dan 3 x zoveel als nr 2 apache/activemq 7.009			  
select wl.project, count(project) as aantal
from wijziging_lineage wl
where wl.commitid in (select distinct c.id 
					   from commitinfo c
					   where c.id in (select distinct commitid
					   				 from wijziging_lineage wl
					   				 where falsepositive = false
					   				)
					   and cast(date_part('year',commitdatumtijd) as int) = 2007)
group by wl.project
order by aantal desc;

-- hoeveel commits heeft een project verdeeld per jaar?
-- id 60803 openjdk/shenandoah
select cast(date_part('year',commitdatumtijd) as int) as jaar, count(cast(date_part('year',commitdatumtijd) as int)) as aantal
from wijziging_lineage wl
    ,commitinfo c 
where wl.commitid = c.id
and wl.projectid = 60803
and wl.falsepositive = false
group by cast(date_part('year',commitdatumtijd) as int)
order by jaar asc;


