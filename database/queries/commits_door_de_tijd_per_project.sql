CREATE TABLE IF NOT EXISTS compare_project_history
( idproject bigint not null
 ,count_commit int
 ,count_mc_commit int
 ,avg_commit decimal
 ,avg_mc_commit decimal
 ,eerste_mc_commit int
 ,laatste_mc_commit int
 ,laatste_commit int
 ,eerste_commit_datum date
 ,eerste_mc_datum date
 ,laatste_mc_datum date
 ,laatste_commit_datum date
 ,CONSTRAINT compare_project_history_pkey PRIMARY KEY(idproject)
 )
TABLESPACE pg_default;

-- herbeginnen
truncate table compare_project_history

-- insert totalen 
insert into compare_project_history(idproject, count_commit, avg_commit, laatste_commit, eerste_commit_datum, laatste_commit_datum)  
select idproject, count(volgnummer) as count_commit, avg(volgnummer) as avg_commit, max(volgnummer) as laatste_commit,
	   min(commitdatumtijd) as eerste_commit_datum, max(commitdatumtijd) as laatste_commit_datum
from commit_volgorde cv 
group by idproject
order by idproject; 

-- update met multi-core gegevens
update compare_project_history
set (count_mc_commit, avg_mc_commit, eerste_mc_commit, laatste_mc_commit, eerste_mc_datum, laatste_mc_datum) = 
	(select count(volgnummer) as count_mc_commit, 
            avg(volgnummer) as avg_mc_commit, 
            min(volgnummer) as eerste_mc_commit, 
            max(volgnummer) as laatste_mc_commit,
	        min(commitdatumtijd) as eerste_mc_datum,
	        max(commitdatumtijd) as laatste_mc_datum
	from commit_volgorde cv 
	where idcommit in (select distinct commitid
                	   from wijziging_lineage wl
                 	   where falsepositive = false)
    and cv.idproject = compare_project_history.idproject);

   
-- Toon verdeling van multi-core commits per project.    
-- selecteer percentueel_verschil
-- hoe hoger, des te meer commits aan het begin van het project
-- negatief? Dan is multi-core later toegevoegd  
-- Lijkt een kandidaat voor een bell curve grafiek.                 	
select idproject, count_commit,  ((avg_commit - avg_mc_commit)  / count_commit) * 100 as percentueel_verschil
from compare_project_history where count_mc_commit > 0;

-- Java cijfers:  
-- 449 groter op 735 projecten met multi-core 
-- 292 groter dan 10% 
-- 189 groter dan 20%
-- 110 groter dan 30%
--  49 groter dan 40% ( 6 tot 238 commits)
--   0 groter dan 50%
--  94 precies 0%   ( projecten met heel weinig commits. 1 outlier met 58 )
-- 192 kleiner dan 0%
--  88 kleiner dan -10%
--  50 kleiner dan -20%
--  22 kleiner dan -30%
--  10 kleiner dan -40% ( 15 tot 311 commits)
--   0 kleiner dan -50%
select idproject, count_commit 
from compare_project_history 
where count_mc_commit > 0
and ((avg_commit - avg_mc_commit)  / count_commit) * 100  > 40;

                 	
                 	
