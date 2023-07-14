 -- view om te zien welke wijziging in welke commit, welk project hoort
CREATE OR REPLACE VIEW wijziging_lineage
AS SELECT bz.zoekterm as zoekterm
      ,b.id as bestandswijziging
      ,c.author_id as auteur
      ,p.naam as project
      ,c.id as commitid
      ,p.id as projectid
      ,bz.id AS bestandswijzingzoekterm_id 
from bestandswijziging_zoekterm bz 
right outer join bestandswijziging b on bz.idbestandswijziging = b.id
join commitinfo c on b.idcommit = c.id
join project p on c.idproject = p.id;

-- Permissions
GRANT SELECT ON TABLE wijziging_lineage TO appl;


