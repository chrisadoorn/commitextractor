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

-- alternatieve query via view -- 1516
select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
group by wl.auteur
order by verschillende_zoektermen desc;

select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
where wl.falsepositive = false 
and   wl.uitgesloten = false
group by wl.auteur
having count(distinct zoekterm)> 0
order by verschillende_zoektermen desc; -- 3079

select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
group by wl.auteur
having count(distinct zoekterm)> 9
order by verschillende_zoektermen desc; -- 146

select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
group by wl.auteur
having count(distinct zoekterm)> 19
order by verschillende_zoektermen desc; -- 44

select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
group by wl.auteur
having count(wl.auteur) > 0
order by verschillende_zoektermen desc; -- 44

select count(*) -- 309 controlegetal
from auteur_tellingen at2 
where aantal_bevestigd > 0;

-- false positives nog niet uitgehaald 371
select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct wl.zoekterm) as verschillende_zoektermen
from wijziging_lineage wl
    ,java_parse_result jpr 
where wl.zoekterm = jpr.zoekterm 
and  wl.bestandswijziging = jpr.bw_id 
group by wl.auteur
order by verschillende_zoektermen desc;

-- false positives nog niet uitgehaald, en iets nieuws toegevoegd 277
select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct wl.zoekterm) as verschillende_zoektermen
from wijziging_lineage wl
    ,java_parse_result jpr 
where wl.zoekterm = jpr.zoekterm 
and  wl.bestandswijziging = jpr.bw_id 
and jpr.achteraf_nieuw_usage = true
and jpr.is_in_namespace = true
group by wl.auteur
order by verschillende_zoektermen desc;
