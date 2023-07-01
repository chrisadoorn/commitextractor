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

select * from processor p ;
update processor
set status = 'geblokt'

select distinct(project_id), projectnaam
from handmatige_check hc
order by project_id

select count(*)
from prod.handmatige_check
where gecontroleerd = true;


INSERT INTO selectie
(selectionmoment, "language", commitsminimum, contributorsminimum, excludeforks, onlyforks, hasissues, haspulls, haswiki, haslicense, committedmin, locatie)
VALUES('2023-05-05', 'java', 0, 0, false, false, false, false, false, false, '2023-05-05', 'https://voorbeeld.com/'::character varying);

INSERT INTO project
(naam, idselectie, main_language)
VALUES('kip/ikhebje5', 1, 'java');
select * from verwerk_project vp ;

UPDATE verwerk_project
SET  resultaat='verwerkt', processtap='extractie'
WHERE id=63;

SELECT count(id)
FROM bestandswijziging
where tekstachteraf is not null ;

update processor
set status = 'geblokt'
where status = 'actief';



select  b.tekstvooraf, b.tekstachteraf, p.id as project_id, p.naam as project_naam, bz.zoekterm, bz.id as bwz_id
from    bestandswijziging b,
        commitinfo c,
        project p,
        bestandswijziging_zoekterm bz
where   b.idcommit = c.id
and     c.idproject = p.id
and     bz.idbestandswijziging = b.id
and     bz.falsepositive = false


select b.tekstvooraf
from bestandswijziging b
where b.id = 181379;



select b.tekstachteraf
from bestandswijziging b
where b.id = 181379;


SELECT  project_id, count(project_id)
FROM java_parser_selection_view
group by project_id
order by 2 DESC;

update verwerk_project
set status = 'gereed'
where id != 11;

update verwerk_project
set processtap = 'zoekterm_controleren'
   ,resultaat = 'verwerkt'
   ,processor = null
   ,status = 'gereed'
where processtap = 'java_parsing'
-- and id not in (9,18,26,13)
and id = 11
and resultaat  = 'mislukt'
and id in (select project_id from java_parser_selection_view);

select count(*) from bestandswijziging_zoekterm bz;                             -- 53049 alle gevonden keywords
select count(*) from bestandswijziging_zoekterm bz where falsepositive = true;  -- 40573
select count(*) from bestandswijziging_zoekterm bz where falsepositive = false; -- 12476
select count(*) from java_parser_selection_view jpsv;                           -- 53049
select count(*) from java_parse_result jpr ;                                    -- 53032 + 17 parse errors = 50279, missend: 2770
select count(*) from java_parse_result jpr where bevat_unknown = true; -- 0
select count(*) from java_parse_result jpr where is_verwijderd = true; -- 1721
select count(*) from java_parse_result jpr where is_in_namespace = true; -- 30052
select count(*) from java_parse_result jpr where is_gebruik_gewijzigd = true; -- 12018
select count(*) from java_parse_result jpr where length(usage_list_achteraf)> 2 and is_in_namespace = false; -- 6612 --
select count(*) from java_parse_result jpr where length(usage_list_achteraf)= 2 and is_in_namespace = false; -- 16783  -- false positives:
select count(*) from java_parse_result jpr where is_nieuw = true; -- 6970 13% Dit is niet in lijn met hoe normale ontwikkeling gaat. Je schrijft niet in 1 keer perfecte code.
select count(*) from compare_analysis v where v.falsepositive = false and is_nieuw = true; --4401 = 35% van 12476
select count(*) from compare_analysis v where v.falsepositive = false and is_nieuw = false and is_gebruik_gewijzigd = true; -- 3066 van 12476 = 24%
select count(*) from bestandswijziging b where b.tekstvooraf is null; -- 36911 13%
select count(*) from bestandswijziging b; -- 275173

select project_id, count(project_id) from java_parser_selection_view jpsv
where id not in (select id from java_parse_result jpr)
group by project_id

select count(id) from java_parse_result
where is_in_gebruik = false and is_gebruik_gewijzigd = true not

select zoekterm, count(zoekterm)
from java_parser_selection_view jpsv
where jpsv.id not in (select id from java_parse_result jpr)
group by zoekterm

-- meest gebruikte zoektermen
select zoekterm, count(zoekterm)
from java_parse_result jpsv
group by zoekterm
order by 2 DESC

-- niet gebruikte zoektermen
select z.zoekwoord
from zoekterm z
where zoekwoord not in (select distinct(jpr.zoekterm)  from java_parse_result jpr)