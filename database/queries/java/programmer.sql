
-- verhoudingsgewijs meer verwijderd? 
select count(*) from bestandswijziging b  -- 2072141 totaal
-- uitsluiten van gevallen waar het zoekwoord in een andere namespace stond

select count (distinct author_id)
from commitinfo c ;
