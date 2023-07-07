select count(*) from project p ;
select count(*) from verwerk_project vp ;

-- maak een sample uit 93.718 projecten
-- sluit eerst alles uit
update verwerk_project set status = 'geblokt';

-- zet alleen aan waarbij (mod (86) + 1) == 0 
-- + 1, want 2e run.
update verwerk_project set status = 'nieuw'
where mod(id, 86)  = 1::bigint;

-- controleer dat de gewenste sample size is bereikt ( bij benadering) 1090 = OK
select count(*) from verwerk_project vp
where status = 'nieuw';

-- maak een nieuwe selectie voor de overgebleven projecten
-- id van selectie moet opgezocht worden, om in de insert te gebruiken 
select id from selectie;
INSERT INTO selectie
(selectionmoment, "language", commitsminimum, contributorsminimum, excludeforks, onlyforks, hasissues, haspulls, haswiki, haslicense, committedmin)
SELECT  selectionmoment, "language", commitsminimum, contributorsminimum, excludeforks, onlyforks, hasissues, haspulls, haswiki, haslicense, committedmin
FROM selectie where id = 1;

-- koppel projecten aan nieuwe selectie
update project 
set idselectie = (select max(id) from selectie)
where id in (select id 
               from verwerk_project 
               where status = 'geblokt');


