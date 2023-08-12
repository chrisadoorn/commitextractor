--SQ.2 What is the correlation between multi-core programming primitives and the
-- percentage of programmers using them?

-- hoe vaak wordt welke zoekterm gebruikt?
select wl.zoekterm , count(wl.zoekterm) as aantal_gebruik 
from wijziging_lineage wl
where wl.falsepositive = false 
and   wl.uitgesloten = false 
group by wl.zoekterm
order by aantal_gebruik desc;

-- door hoeveel auteurs wordt een zoekterm gebruikt?
select wl.zoekterm , count(distinct wl.auteur) as aantal_auteurs 
from wijziging_lineage wl
where wl.falsepositive = false 
and   wl.uitgesloten = false 
group by wl.zoekterm
order by aantal_auteurs desc;

-- hoeveel verschillende zoektermen gebruikt een enkele auteur?
select wl.auteur, count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl
where wl.falsepositive = false 
and   wl.uitgesloten = false
group by wl.auteur
order by verschillende_zoektermen desc;

-- aantal auteurs die x verschillende zoektermen gebruiken. 
select sq.verschillende_zoektermen, count(sq.verschillende_zoektermen)
from ( select wl.auteur as auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen 
		from wijziging_lineage wl 
		where wl.falsepositive = false 
		and   wl.uitgesloten = false
		group by wl.auteur) as sq
group by sq.verschillende_zoektermen
order by sq.verschillende_zoektermen desc;

