-- alle authors
select count(distinct author_id) from commitinfo c -- 1911

-- authors die multi-core commit uitvoeren
select count(distinct author_id)                  -- 660 = 34%
from commitinfo c 
 , java_parse_result jpr 
where jpr.commit_id = c.id

-- geidentifeerde authors
select count(distinct author_id)                  -- 496 = 26% van alles
from commitinfo c                                 --     = 75% van authors die mc doen
 , java_parse_result jpr 
where jpr.commit_id = c.id
and author_id < 900000000;

   
    
-- view om parse result met bestandswijziging te combineren
select count(*) --bl., jpr.zoekterm, jpr.bw_id
from bestandswijziging_lineage bl 
left join java_parse_result jpr on bl.bestandswijziging  = jpr.bw_id ; 
select count(*) from java_parse_result; 
select count(*) from commitinfo c; -- 74396
select count(*) from wijziging_lineage bl; --299109 
select count(*) from bestandswijziging; --275173
select count(*) from wijziging_lineage bl
where bl.zoekterm is null; --246060 
select count(*) from wijziging_lineage bl
where bl.zoekterm is not null; -- 53049

-- aantallen commits per auteur per project 
select count(author_id), author_id, idproject                  -- 660 = 34%
from commitinfo c 
group by idproject, author_id
order by idproject, author_id;

select author_id, idproject,
		(select count(jpr.commit_id) from java_parse_result jpr 
		  where jpr.commit_id in (select )
		)
from commitinfo c
group by idproject, author_id
order by idproject, author_id;

-- aantallen multi-core commits per auteur per project ( zijn  er verhoudingsverschillen tussen projecten? )
select count(auteur)
from wijziging_lineage wl
where zoekterm is not null
group by auteur, project;

-- select andere commits per auteur per project 
select count(auteur), auteur, project
from wijziging_lineage wl
where zoekterm is null
group by auteur, project;




-- aanpasingen in verhouding tot tijdsduur project

-- mc aanpassingen in verhouding tot andere aanpassingen
