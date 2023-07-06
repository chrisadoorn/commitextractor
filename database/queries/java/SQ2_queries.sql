--SQ.2 What is the correlation between multi-core programming primitives and the
-- percentage of programmers using them?

-- Query:
select b.author_id, count(distinct(d.zoekterm)) as verschillende_zoektermen
	from project a,
     commitinfo b,
     bestandswijziging c,
     bestandswijziging_zoekterm d
	where a.id = b.idproject
        and b.id = c.idcommit
        and c.id = d.idbestandswijziging
group by b.author_id
order by verschillende_zoektermen desc;

-- auteurs met meer dan 50 zoekwoorden, werkten bij 2 projecten.(google/guava, google/error-prone) $ bij beide. De 2 onbekende auteurs alleen bij google/guava.
select * from auteur_tellingen at2 where auteur in (1703908, 900047421, 900014786, 478458, 101568, 2036304 )
order by auteur ;

select wl.auteur, count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
group by wl.auteur
order by verschillende_zoektermen desc;