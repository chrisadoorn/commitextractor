-- alle authors
select count(distinct author_id) from commitinfo c -- 1911
select count(distinct auteur) from auteur_tellingen at2  -- 1515
select count( distinct c.author_id)
from commitinfo c
where author_id not in (select distinct auteur from auteur_tellingen); -- 396
-- auteurs die geen bestandswijzigingen hebben, dat wil zeggen: ze hebben geen (java) code geschreven.
-- bevestigd met onderstaande query.  
select count( distinct c.author_id), distinct author_id , p.naam, p.id as projectid 
from commitinfo c
    ,project p
    ,bestandswijziging b 
where p.id = c.idproject 
and   b.idcommit = c.id 
and author_id not in (select distinct auteur from auteur_tellingen)
order by p.id; -- 0 
              

-- authors die multi-core commit uitvoeren
select count(distinct auteur)                  -- 301 op 1515  = 19.9%
from auteur_tellingen at2 
where aantal_bevestigd > 0;

-- alle bestandswijzigingen
select sum(aantal_totaal)
from auteur_tellingen at2; -- 273.261
-- waarvan door multi-core programmeurs 233.547 85.5%
select sum(aantal_totaal)
from auteur_tellingen at2
where auteur in (select distinct auteur
				 from auteur_tellingen at2 
				 where aantal_bevestigd > 0);
-- en de rest is dus : 39.714 14.5%
select sum(aantal_totaal)
from auteur_tellingen at2
where auteur not in (select distinct auteur
				     from auteur_tellingen at2 
				     where aantal_bevestigd > 0);
				
-- aantal auteurs per project
select projectid, count(auteur) as aantal_auteurs, sum(aantal_totaal) as bestandswijzing_per_project
from   auteur_tellingen at2 
group by at2.projectid
order by 2 desc; 				    
				    
-- aantal multi-core auteurs per project, aantal en percentage multi-core wijzigingen per project.
select projectid, count(auteur) as multi_core_auteurs, sum(aantal_totaal) as bestandswijzing_per_project, sum(aantal_bevestigd) as multicore_wijziging,
       to_char((( sum(aantal_bevestigd)::dec / sum(aantal_totaal)::dec )* 100), '999.99') as perc_multicore,
       to_char(( sum(aantal_bevestigd)::dec / count(auteur)::dec ), '999.99') as multicore_per_auteur
from   auteur_tellingen at2 
where auteur in (select distinct auteur
				     from auteur_tellingen at2 
				     where aantal_bevestigd > 0)
group by at2.projectid
order by projectid; 	

-- aantal aantal en percentage multi-core wijzigingen per multi-core auteur.
select auteur, count(auteur) as multi_core_auteurs, sum(aantal_totaal) as bestandswijzing_per_auteur, sum(aantal_bevestigd) as multicore_wijziging,
       to_char((( sum(aantal_bevestigd)::dec / sum(aantal_totaal)::dec )* 100), '999.99') as perc_multicore
from   auteur_tellingen at2 
where auteur in (select distinct auteur
				     from auteur_tellingen at2 
				     where aantal_bevestigd > 0)				     
group by at2.auteur
-- having clause geeft 13 auteurs die uitsluitend multi-core geprogrammeerd hebben (5x1, 3x 2, 1x3, 3x4 en 1x15)
-- 1x 15 = 114485052, microsoft/mssql-jdbc wat 71 programmeurs heeft, 
--having sum(aantal_totaal) = sum(aantal_bevestigd)
order by at2.auteur; 	

-- de auteur met 15 bestandswijzigingen, alle multi-core
select * from auteur_tellingen at2 where auteur = 66626;				    

-- geidentifeerde authors
select count(distinct author_id)                  -- 496 = 26% van alles
from commitinfo c                                 --     = 75% van authors die mc doen
 , java_parse_result jpr 
where jpr.commit_id = c.id
and author_id < 900000000;

   
    
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
select count(auteur), project 
from wijziging_lineage wl
where zoekterm is not null
group by auteur, project
order by project ;

-- select andere commits per auteur per project 
select count(auteur), auteur, project
from wijziging_lineage wl
where zoekterm is null
group by auteur, project;


select sum(aantal_kandidaat)
from auteur_tellingen at2 

-- aanpasingen in verhouding tot tijdsduur project

-- mc aanpassingen in verhouding tot andere aanpassingen
