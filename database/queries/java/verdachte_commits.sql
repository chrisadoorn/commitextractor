
-- commits die alleen bestandswijzigingen bevatten waarin iets nieuws is toegevoegd ( aantal)
select count(distinct idcommit) as aantal_commits_alleen_nieuw  -- 15682 op 303330 = 5.2%
from bestandswijziging b  
where idcommit not in ( select distinct idcommit
                      from bestandswijziging b2
                      where b2.tekstvooraf is not null);  
                     


-- commits die alleen bestandswijzigingen bevatten waarin iets nieuws is toegevoegd 
-- met aantal bestandswijzigingen, aflopen geordend
select idcommit, count(idcommit) as aantal, remark
from bestandswijziging b
where idcommit not in ( select distinct idcommit
                      from bestandswijziging b2
                      where b2.tekstvooraf is not null)
group by idcommit
order by aantal desc
 ;
-- aantallen per segment, speel met having clause
--  aantal > 5.000	:	3 (max = 11.363)
--  aantal >= 1.000	:	35 
--  aantal >=  500	:	23
--  aantal >=  300	:	36
--  aantal >=  200	:	140
select idcommit, count(idcommit) as aantal
from bestandswijziging b  
where idcommit not in ( select distinct idcommit
                      from bestandswijziging b2
                      where b2.tekstvooraf is not null)
group by idcommit
having count(idcommit) < 3500
and    count(idcommit) > 199
order by aantal desc
 ;

-- verdachte commits met remark
select id, remark
from commitinfo c  
where id in ( select idcommit as aantal
from bestandswijziging b  
where idcommit not in ( select distinct idcommit
                      from bestandswijziging b2
                      where b2.tekstvooraf is not null)
group by idcommit
having count(idcommit) < 35000
and    count(idcommit) > 999
order by aantal desc );



select count(distinct idcommit) as aantal_commits_met_wijzigingen -- 287648 commits met wijzigingen op 303330 = 94.8%
  from bestandswijziging b2     
  where b2.tekstvooraf is not null;
select count(id) as aantal_bestandswijzigingen_in_commits_met_wijzigingen -- 1610487 commits met wijzigingen op 2072141 = 77.7%
  from bestandswijziging b2     
  where b2.tekstvooraf is not null;
 
 


select count(id) as aantal_bestandswijzigingen_in_commits_alleen_nieuw  -- 229038 op 2072141 = 11.1%
from bestandswijziging b  
where b.tekstvooraf is null
and idcommit not in ( select distinct idcommit
                      from bestandswijziging b2
                      where b2.tekstvooraf is not null);  
