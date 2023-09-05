-- Calculation ( from https://www.socscistatistics.com/confidenceinterval/default2.aspx )
-- 
-- aantal N = 10383
-- gemiddelde M = 212.6
-- standaard deviatie binnen sample std = 1541.3
       
-- t-value for confidence of 95%  t = 1.96 
-- sM = √( (std * std) /M) 
-- sM = √((1541.3 * 1541.3)/10383) = 15.13

-- μ = M ± t(sM)
-- μ = 212.6 ± 1.96*15.13
-- μ = 212.6 ± 29.6      
       

-- filechanges by programmer
select count(distinct auteur) as aantal_n
from auteur_tellingen at2;  -- java 10383

select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
       group by auteur) as subquery ;  -- java 212

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_all
 FROM   (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
       group by auteur) as subquery; -- java: 1541.3

       
-- mc file changes by all programmer
select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_bevestigd) as som_per_auteur
      from auteur_tellingen
       group by auteur) as subquery ; -- 7.7     

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_all
 FROM   (select sum(aantal_bevestigd) as som_per_auteur
      from auteur_tellingen
       group by auteur) as subquery; -- java: 72.3

-- filechanges by mc programmer
select count(distinct auteur) as aantal_mc
from auteur_tellingen at2
where auteur in (select distinct auteur
				 from auteur_tellingen at2
                 where aantal_bevestigd > 0);         
 
select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  group by auteur) as subquery ;

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_mc
from (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  group by auteur) as subquery ;

-- mc filechanges by mc programmer	 
select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_bevestigd) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  group by auteur) as subquery ;

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_mc
from (select sum(aantal_bevestigd) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  group by auteur) as subquery ;	 
	 
-- filechanges by non mc programmer	 
select count(distinct auteur) as aantal_mc
from auteur_tellingen at2
where auteur not in (select distinct auteur
				 from auteur_tellingen at2
                 where aantal_bevestigd > 0);         
 
select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
      where auteur not in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  group by auteur) as subquery ;

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_mc
from (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
      where auteur not in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  group by auteur) as subquery ;	 

	 
-- filechanges by identified mc authors
select count(distinct auteur) as aantal_mc
from auteur_tellingen at2
where auteur in (select distinct auteur
				 from auteur_tellingen at2
                 where aantal_bevestigd > 0)        
and auteur < 900000000;

select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  and auteur < 900000000
	  group by auteur) as subquery ;

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_mc
from (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  and auteur < 900000000
	  group by auteur) as subquery ;

-- mc filechanges by identified mc programmer	 
select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_bevestigd) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  and auteur < 900000000
	  group by auteur) as subquery ;

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_mc
from (select sum(aantal_bevestigd) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  and auteur < 900000000
	  group by auteur) as subquery ;	 

-- filechanges by not identified mc authors
select count(distinct auteur) as aantal_mc
from auteur_tellingen at2
where auteur in (select distinct auteur
				 from auteur_tellingen at2
                 where aantal_bevestigd > 0)        
and auteur > 900000000;

select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  and auteur > 900000000
	  group by auteur) as subquery ;

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_mc
from (select sum(aantal_totaal) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  and auteur > 900000000
	  group by auteur) as subquery ;

-- mc filechanges by identified mc programmer	 
select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_bevestigd) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  and auteur > 900000000
	  group by auteur) as subquery ;

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_mc
from (select sum(aantal_bevestigd) as som_per_auteur
      from auteur_tellingen
      where auteur in (select distinct auteur
						from auteur_tellingen at2
						where aantal_bevestigd > 0)
	  and auteur > 900000000
	  group by auteur) as subquery ;	
	 
-- all not suspicious	 
select count(distinct auteur) as aantal_n
from auteur_tellingen at2
where aantal_ns_totaal > 0;

select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_ns_totaal) as som_per_auteur
      from auteur_tellingen
      where aantal_ns_totaal > 0
      group by auteur) as subquery ;  

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_all
from (select sum(aantal_ns_totaal) as som_per_auteur
      from auteur_tellingen
      where aantal_ns_totaal > 0
      group by auteur) as subquery ;  

-- mc file changes by all programmer not suspicious
select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_ns_bevestigd) as som_per_auteur
       from auteur_tellingen
       where aantal_ns_totaal > 0
       group by auteur) as subquery ; 

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_all
 FROM   (select sum(aantal_ns_bevestigd) as som_per_auteur
      from auteur_tellingen
      where aantal_ns_totaal > 0
       group by auteur) as subquery; 

-- all not suspicious by mc programmers	 
select count(distinct auteur) as aantal_n
from auteur_tellingen at2
where aantal_ns_totaal > 0
and aantal_ns_bevestigd > 0;

select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_ns_totaal) as som_per_auteur
      from auteur_tellingen
      where aantal_ns_totaal > 0
      and aantal_ns_bevestigd > 0
      group by auteur) as subquery ;  

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_all
from (select sum(aantal_ns_totaal) as som_per_auteur
      from auteur_tellingen
      where aantal_ns_totaal > 0
      and aantal_ns_bevestigd > 0
      group by auteur) as subquery ;  

-- mc file changes by all mc programmer not suspicious
select AVG(som_per_auteur) 
as gemiddelde_wijzigingen
from (select sum(aantal_ns_bevestigd) as som_per_auteur
       from auteur_tellingen
       where aantal_ns_totaal > 0
       and aantal_ns_bevestigd > 0
       group by auteur) as subquery ; 

SELECT ROUND(STDDEV(som_per_auteur), 2) 
AS standard_deviation_all
 FROM   (select sum(aantal_ns_bevestigd) as som_per_auteur
      from auteur_tellingen
      where aantal_ns_totaal > 0
       and aantal_ns_bevestigd > 0
       group by auteur) as subquery; 

-- only suspicious 
select count(distinct author_id) as number_of_programmers
from commitinfo c 
where id in (select idcommit
             from suspicious_commit sc
             where sc.aantal > 99);

select AVG(file_changes)
as gemiddelde_wijzigingen
from (
		select count(distinct bestandswijziging) as file_changes
		from wijziging_lineage wl 
		where commitid in (select idcommit
		                   from suspicious_commit sc
		                   where sc.aantal > 99)
		group by auteur
	) as subquery ;   

select ROUND(STDDEV(file_changes), 2) 
as standard_deviation
from (
		select count(distinct bestandswijziging) as file_changes
		from wijziging_lineage wl 
		where commitid in (select idcommit
		                   from suspicious_commit sc
		                   where sc.aantal > 99)
		group by auteur
	) as subquery ; 
            
            
select AVG(file_changes)
as gemiddelde_wijzigingen
from (
		select count(distinct bestandswijziging) as file_changes, auteur
		from wijziging_lineage wl 
		where commitid in (select idcommit
		                   from suspicious_commit sc
		                   where sc.aantal > 99)
		and falsepositive = false 
		and uitgesloten = false
		group by auteur
		union all 
		select 0, auteur
		from wijziging_lineage wl 
		where commitid in (select idcommit
		                   from suspicious_commit sc
		                   where sc.aantal > 99)
		and auteur not in (select  auteur
							from wijziging_lineage wl 
							where commitid in (select idcommit
							                   from suspicious_commit sc
							                   where sc.aantal > 99)
							and falsepositive = false 
							and uitgesloten = false
							group by auteur)
		group by auteur
	) as subquery ;          


select ROUND(STDDEV(file_changes), 2) 
as standard_deviation
from (
		select count(distinct bestandswijziging) as file_changes, auteur
		from wijziging_lineage wl 
		where commitid in (select idcommit
		                   from suspicious_commit sc
		                   where sc.aantal > 99)
		and falsepositive = false 
		and uitgesloten = false
		group by auteur
		union all 
		select 0, auteur
		from wijziging_lineage wl 
		where commitid in (select idcommit
		                   from suspicious_commit sc
		                   where sc.aantal > 99)
		and auteur not in (select  auteur
							from wijziging_lineage wl 
							where commitid in (select idcommit
							                   from suspicious_commit sc
							                   where sc.aantal > 99)
							and falsepositive = false 
							and uitgesloten = false
							group by auteur)
		group by auteur
	) as subquery ;          
       