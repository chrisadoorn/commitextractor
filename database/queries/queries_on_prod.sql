select id
from commitinfo c 
where c.id not in ( select distinct(idcommit) from bestandswijziging b)

alter or create materialized view commit_met_inhoud as
	 select distinct(idcommit) as idcommit from bestandswijziging b
	 order by idcommit
with no data;	


select count(*) from commit_met_inhoud; -- 234229
select count(*) from commitinfo c;      -- 549096
select count(*) from commitinfo c
where id not in (select idcommit from commit_met_inhoud)


