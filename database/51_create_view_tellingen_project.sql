-- View: test.tellingen_project

-- DROP VIEW test.tellingen_project;

CREATE OR REPLACE VIEW test.tellingen_project
 AS
 SELECT p.id,
    p.naam,
    ( SELECT count(c.idproject) AS commit_aantal
           FROM test.commitinfo c
          WHERE c.idproject = p.id
          GROUP BY c.idproject) AS commit_aantal,
    ( SELECT count(b.idcommit) AS bestandswijzing_aantal
           FROM test.bestandswijziging b
          WHERE (b.idcommit IN ( SELECT c.id
                   FROM test.commitinfo c
                  WHERE c.idproject = p.id))) AS bestandswijzing_aantal,
    null AS programmeurs_aantal
   FROM test.project p
  ORDER BY (( SELECT count(c.idproject) AS commit_aantal
           FROM test.commitinfo c
          WHERE c.idproject = p.id
          GROUP BY c.idproject));

ALTER TABLE test.tellingen_project
    OWNER TO postgres;
COMMENT ON VIEW test.tellingen_project
    IS 'Toont sommaties voor projecten. ';

GRANT SELECT ON TABLE test.tellingen_project TO appl;
GRANT ALL ON TABLE test.tellingen_project TO postgres;

