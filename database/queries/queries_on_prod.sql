select id
from commitinfo c 
where c.id not in ( select distinct(idcommit) from bestandswijziging b)

-- selecteer een aantal metrieken
SELECT id, naam,
main_language,
cast(languages::json->>'Java' as int) as java_bytes,
cast(languages::json->>'Java' as int) / 1024  as java_kb,
project_size as project_kb,
contributors,
number_of_languages,
languages
	FROM project
	order by number_of_languages desc;



alter or create materialized view commit_met_inhoud as
	 select distinct(idcommit) as idcommit from bestandswijziging b
	 order by idcommit
with no data;	


select count(*) from commit_met_inhoud; -- 234229
select count(*) from commitinfo c;      -- 549096
select count(*) from commitinfo c
where id not in (select idcommit from commit_met_inhoud)


