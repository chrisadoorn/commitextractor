
-- queries: all filechanges 
select count(*)  as total from bestandswijziging b
where b.uitgesloten = false;  

select count(*)  as new_file from bestandswijziging b
where tekstvooraf is null
and b.uitgesloten = false;  
  
-- omkering: hoe zit het met de verwijderingen? 
select count(*) as removed from bestandswijziging b
where tekstachteraf is null; 


-- queries: all multi-core filechanges 
-- controle: deze count moet gelijk zijn aan de count van bestandswijziging
select count(distinct bestandswijziging)  as total from wijziging_lineage wl ;
select count(distinct bestandswijziging)  as total 
from wijziging_lineage wl
    ,bestandswijziging b 
where b.id = wl.bestandswijziging 
and   falsepositive = false
and b.uitgesloten = false;  
;

select count(distinct bestandswijziging)  as new_file 
from wijziging_lineage wl
    ,bestandswijziging b 
where b.id = wl.bestandswijziging 
and   falsepositive = false
and tekstvooraf is null
and b.uitgesloten = false;  


-- queries: filechanges with multi-core or removed
select count(distinct bestandswijziging)  as total 
from wijziging_lineage wl
    ,bestandswijziging b 
where b.id = wl.bestandswijziging 
-- onderstaande constructie is omslachtig, 
-- maar hiermee wordt een tablescan op de bestandswijziging tabel voorkomen
-- door een kleine selectie af te dwingen op de is not null constructie
and   falsepositive  is not null
and  (falsepositive = false  
or tekstachteraf is null);

select count(distinct bestandswijziging)  as removed 
from wijziging_lineage wl
    ,bestandswijziging b 
where b.id = wl.bestandswijziging 
and falsepositive is not null  
and tekstachteraf is null;



-- controle queries: false positie en geen multi-core kandidaat tellen. De 3 kunnen hoger zijn dan het totaal aan bestandswijzigingen
-- een bestandswijziging kan voor keywoord Executor false zijn, maar voor ExecutorFactory positief, waardoor dezelfde bestandswijziging
-- zowel in false als in true geteld wordt
select count(distinct bestandswijziging)  as total from wijziging_lineage wl
where falsepositive = true;
select count(distinct bestandswijziging)  as total from wijziging_lineage wl
where falsepositive is null;


