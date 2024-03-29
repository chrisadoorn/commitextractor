-- query 1a : all programmers
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2;

-- query 1b: all programmers
select sum(aantal_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2;

-- query 2a: multi-core
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
from auteur_tellingen at2
where aantal_bevestigd > 0);
-- query 2b: multi-core
select sum(aantal_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
from auteur_tellingen at2
where aantal_bevestigd > 0);

-- query 3a: non multi-core
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where auteur not in (select distinct auteur
from auteur_tellingen at2
where aantal_bevestigd > 0);
-- query 3b: non multi-core n.v.t 

-- query 4a: identified multi-core programmers
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
		from auteur_tellingen at2
		where aantal_bevestigd > 0)
and auteur < 900000000;
-- query 4b: identified multi-core programmers
select sum(aantal_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
		from auteur_tellingen at2
		where aantal_bevestigd > 0)
and auteur < 900000000;

-- query 5a: unidentified multi-core programmers
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
		from auteur_tellingen at2
		where aantal_bevestigd > 0)
and auteur > 900000000;
-- query 5b: unidentified multi-core programmers
select sum(aantal_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
		from auteur_tellingen at2
		where aantal_bevestigd > 0)
and auteur > 900000000;

-- query 6a uitsluiting suspicious commits totaal:
select count(distinct auteur) as number_of_programmers, sum(aantal_ns_totaal) as file_changes, 
to_char(( sum(aantal_ns_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where aantal_ns_totaal > 0;

--query 6b: 
select sum(aantal_ns_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_ns_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2
where aantal_ns_totaal > 0;

-- query 7a uitsluiting suspicious commits multi-core:
select count(distinct auteur) as number_of_programmers, sum(aantal_ns_totaal) as file_changes, 
to_char(( sum(aantal_ns_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
from auteur_tellingen at2
where aantal_ns_bevestigd > 0)
and aantal_ns_totaal > 0;
-- query 7b  uitsluiting suspicious commits multi-core:
select sum(aantal_ns_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_ns_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
from auteur_tellingen at2
where aantal_ns_bevestigd > 0)
and aantal_ns_totaal > 0;


-- query 8 uitsluitend suspicious commits totaal:
select count(distinct author_id) as number_of_programmers
from commitinfo c 
where id in (select idcommit
             from suspicious_commit sc
             where sc.aantal > 99);

select count(idcommit) as file_changes
from bestandswijziging b 
where idcommit in (select idcommit
                   from suspicious_commit sc
                   where sc.aantal > 99);

-- deel file_changes door number_of_programmers voor file changes by programmer
select count(distinct bestandswijziging) as multi_core_file_change
from wijziging_lineage wl 
where falsepositive = false 
and uitgesloten = false
and commitid in (select idcommit
                   from suspicious_commit sc
                   where sc.aantal > 99);
                  
-- deel multi_core_file_change door number_of_programmers voor multi core file changes by programmer

-- query 9a: alles included moved files 
select count(distinct(wl.auteur)) as number_of_programmers
	from wijziging_lineage wl
	where wl.uitgesloten = false
                  
select count(distinct(bestandswijziging)) as file_changes
	from wijziging_lineage wl
	where wl.uitgesloten = false
	     
-- deel file_changes door number_of_programmers voor file changes by programmer
-- omdat verplaatste bestanden niet uitmaken, voor aantal gevonden multi-core commits, dit uit 1b overnemen. 