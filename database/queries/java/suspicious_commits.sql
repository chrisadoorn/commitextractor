-- id ommit met nieuwe bestanden
select count( distinct idcommit  )
from bestandswijziging b 
where tekstvooraf is null; -- 65179 van 335060 = 19,5%

-- met gewijzigde/verwijderde betanden
select count( distinct idcommit  )
from bestandswijziging b 
where tekstvooraf is not null; -- 317670 van 335060

-- met alleen nieuwe bestanden -- 17390 potentieel, 314 > 99 
select idcommit, count(idcommit) as aantal 
from bestandswijziging b 
where tekstvooraf is null
and idcommit not in (select distinct idcommit
					from bestandswijziging b 
					where tekstvooraf is not null)
group by idcommit
-- having count(idcommit) > 99
order by aantal desc 
;

-- commits grote aantallen bestandswijzigingen die niet in suspicious zitten 
select c.id, c.remark
from commitinfo c
where c.id not in (select idcommit from suspicious_commit sc)
and c.id in (select idcommit
					from bestandswijziging b 
					group by idcommit
					having count(idcommit) > 199
					order by count(idcommit))
;
-- er zijn 3271 commits met meer 99 bestandswijzigingen.
-- 314 daarvan zijn alleen nieuw = 9,6% Lager dan over geheel, maar dat ligt voor de hand. de meeste commits met alleen nieuw zijn kleine commits 
select count(idcommit) as aantal, idcommit 
from bestandswijziging b 
group by idcommit
having count(idcommit) > 99
order by aantal desc

select * -- 40814 bestanden, 40812 nieuw, 2 verwijderd 
from bestandswijziging 
where idcommit = 692698
and tekstvooraf is null;


-- suppose cutoff point at 100 --> 405 commits excluded. 
select id, sc.aantal, remark
from commitinfo c,
	suspicious_commit sc 
where c.id = sc.idcommit
and sc.aantal > 99
order by sc.aantal desc ;

-- sluit 266.460 bestandswijzigingen uit
select count(idcommit)
from bestandswijziging b 
where idcommit in (select idcommit
                   from suspicious_commit sc
                   where sc.aantal > 99)


-- hoe vaak worden zoektermen gebruikt?  125.720 vs 102.826 zonder susp. commits
-- hoe vaak worden bestandswijzingingen gebruikt?  79.972 vs 66.978 zonder susp. commits
select count( distinct wl.bestandswijziging) as aantal_gebruik 
from wijziging_lineage wl
where wl.falsepositive = false 
and   wl.uitgesloten = false 
and wl.commitid not in (select idcommit from suspicious_commit sc where sc.aantal > 99)
--group by wl.zoekterm
--order by aantal_gebruik desc;

