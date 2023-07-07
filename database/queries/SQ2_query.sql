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

-- herschreven met gebruik van de view:
select wl.auteur, count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
group by wl.auteur
order by verschillende_zoektermen desc;