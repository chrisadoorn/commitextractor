-- query 1a:
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2;

-- query 1b:
select sum(aantal_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2;

-- query 2a:
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
from auteur_tellingen at2
where aantal_bevestigd > 0);
-- query 2b:
select sum(aantal_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
from auteur_tellingen at2
where aantal_bevestigd > 0);

-- query 3a:
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where auteur not in (select distinct auteur
from auteur_tellingen at2
where aantal_bevestigd > 0);
-- query 3b:

-- query 4a:
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
		from auteur_tellingen at2
		where aantal_bevestigd > 0)
and auteur < 900000000;
-- query 4b:
select sum(aantal_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
		from auteur_tellingen at2
		where aantal_bevestigd > 0)
and auteur < 900000000;

-- query 5a:
select count(distinct auteur) as number_of_programmers, sum(aantal_totaal) as file_changes, 
to_char(( sum(aantal_totaal)::dec / count(distinct auteur)::dec ), '999.99') as avg_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
		from auteur_tellingen at2
		where aantal_bevestigd > 0)
and auteur > 900000000;
-- query 5b:
select sum(aantal_bevestigd) as multi_core_file_change, count(distinct auteur) as number_of_programmers,
to_char(( sum(aantal_bevestigd)::dec / count(distinct auteur)::dec ), '999.99') as avg_mc_programmer
from auteur_tellingen at2
where auteur in (select distinct auteur
		from auteur_tellingen at2
		where aantal_bevestigd > 0)
and auteur > 900000000;
