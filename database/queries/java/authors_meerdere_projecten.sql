-- aantal projecten waaraan een programmeur gewerkt heeft;
select c.author_id, count(distinct p.naam)  as aantal 
from commitinfo c
    ,project p
where c.idproject = p.id
group by  c.author_id
having count(distinct p.naam) > 1
order by author_id desc;

-- 309 auteurs werkten in meerdere projecten, 61 niet geïdentificeerd
-- We missen misschien auteurs die nu dubbel zijn geteld, want gebruik ander emailadres & niet geïdentificeerd.

-- samen 700 combinaties
select auteur, project
from wijziging_lineage 
where auteur in (select subq.auteur 
				from wijziging_lineage subq 
				group by  subq.auteur
				having count(distinct subq.projectid) > 1
				order by subq.auteur desc)
group by auteur, project

-- auteurs en of zij mc hebben geprogrammeerd per project : 647 regels zonder null (niet geselecteerd als kandidaat) 1318 met null
-- false positive is null : niet geselcteerd by text_search
-- false positive = false : dit is multi-core gebruik
-- false positive = true  : vals alarm

create view programmeurs_meerdere_projecten as
select auteur, project, falsepositive, count(*) as aantal, projectid 
from wijziging_lineage 
where auteur in (select subq.auteur 
				from wijziging_lineage subq 
				group by  subq.auteur
				having count(distinct subq.projectid) > 1
				order by subq.auteur desc)
group by auteur, project, projectid , falsepositive 

order by auteur desc, project, falsepositive
;

grant select on programmeurs_meerdere_projecten to appl;

-- 309 auteurs hebben in meerdere projecten gewerkt
-- 201 auteurs hebben hebben in minstens 1 project mc geprogrameerd
-- 108 auteurs hebben nergens mc geprogrameerd     
--  80 auteurs hebben in meerdere projecten mc geprogrammeerd 

-- auteurs die in minstens 1 project multicore hebben geprogrammeerd
select distinct(auteur)
from programmeurs_meerdere_projecten 
where falsepositive = false;	

-- auteurs die geen mc hebben geprogrammeerd
select distinct(auteur)
from programmeurs_meerdere_projecten 
where auteur not in (select distinct(auteur)
						from programmeurs_meerdere_projecten 
						where falsepositive = false);

-- auteurs die in meerdere projecten mc hebben geprogrammeerd.
select auteur, count(auteur)
from programmeurs_meerdere_projecten 
where falsepositive = false
group by auteur
having count(auteur) > 1
order by 2 desc;




-- CONTROLE QUERIES
select * from wijziging_lineage wl where auteur = 900480155
and project = 'microconfig/microconfig-idea-plugin'
order by falsepositive ;

select * from bestandswijziging b 
where id = 2743627;


