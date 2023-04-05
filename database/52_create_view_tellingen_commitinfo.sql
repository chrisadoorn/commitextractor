-- View: test.tellingen_commitinfo

-- DROP VIEW test.tellingen_project;

CREATE OR REPLACE VIEW test.tellingen_commitinfo
 AS
select
c.id, count(b.idcommit) as bestandswijzing_aantal,
'nog te bepalen' as programmeur
from test.commitinfo c
    ,test.bestandswijziging b
where b.idcommit = c.id
group by c.id, b.idcommit;

ALTER TABLE test.tellingen_commitinfo
    OWNER TO postgres;
COMMENT ON VIEW test.tellingen_commitinfo
    IS 'Toont sommaties voor git commits. ';

GRANT SELECT ON TABLE test.tellingen_commitinfo TO appl;
GRANT ALL ON TABLE test.tellingen_commitinfo TO postgres;

