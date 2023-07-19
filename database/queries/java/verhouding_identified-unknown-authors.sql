select count(auteur)        -- 7894 alle auteurs
from auteur_tellingen at2; 
select count(auteur)        -- 1755 auteurs unknown = 22.2%
from auteur_tellingen at2
where auteur >= 900000000;

select count(auteur)        -- 2737 multicore auteurs = 34.6% van alle auteurs doen multi core 
from auteur_tellingen at2
where aantal_bevestigd > 0; 
select count(auteur)        -- 1070 multicore auteurs unknown = 61.0% van alle unknown auteurs doen multi-core
from auteur_tellingen at2
where auteur >= 900000000
and aantal_bevestigd > 0;

