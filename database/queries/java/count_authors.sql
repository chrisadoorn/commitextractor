-- alle authors                                          -- PRD1
select count(distinct author_id) from commitinfo c       -- 10687, 6600 bekend, 4087 onbekend
where author_id > 900000000                              -- 10383, 6602 bekend, 3781 onbekend na opnieuw draaien van author identification 
select count(distinct auteur) from auteur_tellingen at2  -- 7678
select count( distinct c.author_id)
from commitinfo c
where author_id not in (select distinct auteur from auteur_tellingen); -- 0
-- auteurs die geen bestandswijzigingen hebben, dat wil zeggen: ze hebben geen (java) code geschreven.
-- bevestigd met onderstaande query.  
select  distinct author_id , p.naam, p.id as projectid 
from commitinfo c
    ,project p
    ,bestandswijziging b 
where p.id = c.idproject 
and   b.idcommit = c.id 
and author_id not in (select distinct auteur from auteur_tellingen)
order by p.id; -- 0 
              

select count( c.id)
from commitinfo c 
where c.id not in (select distinct idcommit from bestandswijziging b);

-- authors die multi-core commit uitvoeren
select count(distinct auteur)                  -- 2679 op 7678  = 34.9%
from auteur_tellingen at2 
where aantal_bevestigd > 0;

-- alle bestandswijzigingen
select sum(aantal_totaal)
from auteur_tellingen at2; -- 1859203
-- waarvan door multi-core programmeurs 1712989 92.1%
select sum(aantal_totaal)
from auteur_tellingen at2
where auteur in (select distinct auteur
				 from auteur_tellingen at2 
				 where aantal_bevestigd > 0);
-- en de rest is dus : 146214 7.8%
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
having sum(aantal_totaal) = sum(aantal_bevestigd)
order by at2.auteur;

-- aantal bestandswijzigingen, gemiddeld aantal per auteur met multi commit
select sum(aantal_totaal) as aantal_bestandswijzingen, count(distinct auteur) as aantal_programmeurs, 
       to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as gemiddelde
from   auteur_tellingen at2
where auteur in (select distinct auteur
				     from auteur_tellingen at2 
				     where aantal_bevestigd > 0)
and auteur < 900000000;
				    
-- aantal bestandswijzigingen, gemiddeld aantal per auteur met multi commit
select sum(aantal_bevestigd) as aantal_bestandswijzingen, count(distinct auteur) as aantal_programmeurs, 
       to_char(( sum(aantal_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as gemiddelde
from   auteur_tellingen at2
where auteur in (select distinct auteur
				     from auteur_tellingen at2 
				     where aantal_bevestigd > 0)
and auteur < 900000000;
				    				    
				    
				    
-- de auteur met 15 bestandswijzigingen, alle multi-core
select * from auteur_tellingen at2 where auteur = 66626;				    

-- geidentifeerde authors
select count(distinct author_id)                  -- 4923 = 64.1% van alles
from commitinfo c                                 --     = % van authors die mc doen
where 
author_id < 900000000;

-- ongeidentifeerde authors
select count(distinct author_id)                  -- 2755 = 35.8% van alles
from commitinfo c                                 --     = % van authors die mc doen
-- , java_parse_result jpr 
--where jpr.commit_id = c.id
where author_id > 900000000;
   
    									--	PRD1
select count(*) from java_parse_result; 
select count(*) from commitinfo c;         -- 602573
select count(*) from wijziging_lineage bl; --2072141 
select count(*) from bestandswijziging;    --2072141
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
