select count(*) from project p ;
select count(*) from verwerk_project vp ;

-- maak een sample uit 92.029 projecten
-- sluit eerst alles uit
update verwerk_project set status = 'geblokt';

-- zet alleen aan waarbij (mod (86) + 1) == 0 
-- + 1, want 2e run.
update verwerk_project set status = 'nieuw'
where mod(id, 86)  = 1::bigint;

-- controleer dat de gewenste sample size is bereikt ( bij benadering) 1071 = OK
select count(*) from verwerk_project vp
 where vp.resultaat = 'verwerkt'

where status = 'gereed';


