-- id ommit met nieuwe bestanden
select count( distinct idcommit  )
from bestandswijziging b 
where tekstvooraf is null;

-- met gewijzigde/verwijderde betanden
select count( distinct idcommit  )
from bestandswijziging b 
where tekstvooraf is not null;
