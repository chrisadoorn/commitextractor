-- id ommit met nieuwe bestanden
select count( distinct idcommit  )
from bestandswijziging b 
where tekstvooraf is null; -- 65179 van 335060

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