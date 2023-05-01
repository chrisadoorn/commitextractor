-- geselecteerde projecten 
select p.naam from project p;

-- toon verwerking
select vg.project_naam, vg.processtap, vg.resultaat, vg.start_verwerking, vg.einde_verwerking from verwerking_geschiedenis vg;

-- aantal commits 
select count(id) from commitinfo; -- 265

-- aantal bestandswijzigingen
select count(id) from bestandswijziging; -- 651

-- aantal programmeurs per project
select count(distinct author_id) as aantal_programmeurs, idproject  
from commitinfo
group by  idproject  ;

-- aantal commits per programmeur per project 
select c.author_id,  count( p.naam),  p.naam 
from commitinfo c
    ,project p
where c.idproject = p.id
group by author_id,  p.naam 
order by author_id,  p.naam;

-- aantal projecten waaraan een programmeur gewerkt heeft;
select c.author_id, count(distinct p.naam)   
from commitinfo c
    ,project p
where c.idproject = p.id
group by  c.author_id


select bz.zoekterm, count(bz.zoekterm)as aantal 
from bestandswijziging_zoekterm bz
where bz.falsepositive = false 
group by bz.zoekterm 
order by 2 desc;


select bz.zoekterm, b.difftext, b.tekstachteraf  
from bestandswijziging b
    ,bestandswijziging_zoekterm bz 
where bz.idbestandswijziging = b.id 
and bz.falsepositive = true 
limit 1;



select distinct b.extensie 
from bestandswijziging b ;



--reset
delete from  verwerk_project;
delete from  verwerking_geschiedenis;
delete from  processor;
delete from  bestandswijziging_zoekterm;
delete from  bestandswijziging_info;
delete from  bestandswijziging;
delete from  commitinfo;
delete from  project;
delete from  selectie;
