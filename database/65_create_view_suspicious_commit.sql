 -- view toont commitinfo op volgorde, om verder queryen te vereenvoudigen over tijdsduur.
CREATE OR REPLACE VIEW suspicious_commit
AS SELECT b.idcommit,
    count(b.idcommit) AS aantal
   FROM bestandswijziging b
  WHERE b.tekstvooraf IS NULL AND NOT (b.idcommit IN ( SELECT DISTINCT b1.idcommit
           FROM bestandswijziging b1
          WHERE b1.tekstvooraf IS NOT NULL))
  GROUP BY b.idcommit
-- Permissions
GRANT SELECT ON TABLE suspicious_commit TO appl;
       