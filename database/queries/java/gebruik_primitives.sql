-- zoektermen geordend op mogelijk voorkomen: 113
select zoekterm, count(zoekterm) as aantal 
from wijziging_lineage wl
where zoekterm is not null
group by zoekterm
order by aantal desc;

-- zoektermen geordend op actueel voorkomen: 113
select zoekterm, count(zoekterm) as aantal 
from wijziging_lineage wl 
where falsepositive = false
and uitgesloten = false
group by zoekterm
order by aantal desc;


-- zoektermen die niet gevonden zijn: 3 stuks: io.reactivex.rxjava2, io.projectreacto en AsyncBoxView.ChildState
select * 
from java_zoekterm jz 
where jz.zoekterm not in (select jpr.zoekterm 
						  	from java_parse_result jpr
    						  	,bestandswijziging_zoekterm bz 
							where jpr.id = bz.id
							group by jpr.zoekterm);


-- primitives use by programmer
select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
where wl.falsepositive = false 
and   wl.uitgesloten = false
group by wl.auteur
having count(distinct zoekterm)> 0
order by verschillende_zoektermen desc; -- 3079 klopt met aantal mc programmers.


-- primitives use by programmer without suspicious commits
select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
where wl.falsepositive = false 
and   wl.uitgesloten = false
and   wl.commitid not in (select idcommit from suspicious_commit sc)
group by wl.auteur
having count(distinct zoekterm)> 0
order by verschillende_zoektermen desc; -- 2647 klopt niet met aantal mc programmers not suspicious.

-- aantal auteurs die x verschillende zoektermen gebruiken. 
select sq.verschillende_zoektermen, count(sq.verschillende_zoektermen)
from ( select wl.auteur as auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen 
		from wijziging_lineage wl 
		where wl.falsepositive = false 
		and   wl.uitgesloten = false
		group by wl.auteur) as sq
group by sq.verschillende_zoektermen
order by sq.verschillende_zoektermen desc;


-- welke zoektermen worden gebruikt door auteurs die maar 1 zoekterm gebruiken?




-- 10 of meer zoektermen gebruikt
select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
where wl.falsepositive = false 
and   wl.uitgesloten = false
group by wl.auteur
having count(distinct zoekterm)> 9
order by verschillende_zoektermen desc; -- 418

-- 1 tot 3 zoektermen gebruikt
select wl.auteur, count(wl.auteur)as aantal_gebruik ,count(distinct zoekterm) as verschillende_zoektermen
from wijziging_lineage wl 
where wl.falsepositive = false 
and   wl.uitgesloten = false
group by wl.auteur
having count(distinct zoekterm) between 1 and 1
order by verschillende_zoektermen desc; -- 1939 tussen 1 en 3




