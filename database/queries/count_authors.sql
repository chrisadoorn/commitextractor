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
select count(distinct auteur)                  -- 371 op 1515  = 24.5%
from auteur_tellingen at2 
where aantal_bevestigd > 0;

-- alle bestandswijzigingen
select sum(aantal_totaal)
from auteur_tellingen at2; -- 273.261
-- waarvan door multi-core programmeurs 242.558 88.8%
select sum(aantal_totaal)
from auteur_tellingen at2
where auteur in (select distinct auteur
				 from auteur_tellingen at2 
				 where aantal_bevestigd > 0);
-- en de rest is dus : 30.703 11.2%
select sum(aantal_totaal)
from auteur_tellingen at2
where auteur not in (select distinct auteur
				     from auteur_tellingen at2 
				     where aantal_bevestigd > 0);
				
-- aantal auteurs per project
select projectid, count(auteur) as aantal_auteurs, sum(aantal_totaal) as bestandswijzing_per_project
from   auteur_tellingen at2 
group by at2.projectid
order by projectid; 				    
				    
-- aantal multi-core auteurs per project, aantal en percentage multi-core wijzigingen per project.
select projectid, count(auteur) as multi_core_auteurs, sum(aantal_totaal) as bestandswijzing_per_project, sum(aantal_bevestigd) as multicore_wijziging,
       (( sum(aantal_bevestigd)::dec / sum(aantal_totaal)::dec )* 100) as perc_multicore
from   auteur_tellingen at2 
where auteur in (select distinct auteur
				     from auteur_tellingen at2 
				     where aantal_bevestigd > 0)
group by at2.projectid
order by projectid; 	


				    

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
select count(auteur)
from wijziging_lineage wl
where zoekterm is not null
group by auteur, project;

-- select andere commits per auteur per project 
select count(auteur), auteur, project
from wijziging_lineage wl
where zoekterm is null
group by auteur, project;


select sum(aantal_kandidaat)
from auteur_tellingen at2 

update auteur_tellingen as qw
set aantal_totaal = (select count(distinct(wl.bestandswijziging))
	from wijziging_lineage wl
	where qw.auteur = wl.auteur
	and qw.projectid = wl.projectid
) ;

update auteur_tellingen as qw
set aantal_kandidaat = (select count(distinct(wl.bestandswijziging))
	from wijziging_lineage wl
	where qw.auteur = wl.auteur
	and qw.projectid = wl.projectid
	and wl.zoekterm is not null
) ;
-- aanpasingen in verhouding tot tijdsduur project

-- mc aanpassingen in verhouding tot andere aanpassingen
