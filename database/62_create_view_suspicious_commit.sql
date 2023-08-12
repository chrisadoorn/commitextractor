 -- view toont commitinfo op volgorde, om verder queryen te vereenvoudigen over tijdsduur.
CREATE OR REPLACE VIEW suspicious_commit
AS SELECT b.idcommit,
    count(b.idcommit) AS aantal
   FROM bestandswijziging b
  WHERE b.idcommit not IN ( SELECT DISTINCT b1.idcommit
           FROM bestandswijziging b1
          WHERE b1.tekstvooraf IS NOT NULL 
          AND b1.tekstachteraf is not NULL) 
  GROUP BY b.idcommit;
-- Permissions
GRANT SELECT ON TABLE suspicious_commit TO appl;
       

