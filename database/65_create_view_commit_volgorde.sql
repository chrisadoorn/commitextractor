 -- view toont commitinfo op volgorde, om verder queryen te vereenvoudigen over tijdsduur.
CREATE OR REPLACE VIEW commit_volgorde
AS select c.idproject
      ,c.id as idcommit
      ,ROW_NUMBER () over ( partition by c.idproject  order by c.idproject, c.id, c.commitdatumtijd) as volgnummer 
      ,c.commitdatumtijd 
      ,c.hashvalue 
      ,c.author_id
      ,case when c.author_id < 900000000  then 'identified' 
          else 'unknown' 
          end as gebruiker
      ,(select count(b.idcommit)
        from bestandswijziging b
        where b.idcommit = c.id) as aantal_wijzigingen
from commitinfo c
order by c.idproject 
        ,c.id
        ,c.commitdatumtijd; 
      
-- Permissions
GRANT SELECT ON TABLE commit_volgorde TO appl;
       