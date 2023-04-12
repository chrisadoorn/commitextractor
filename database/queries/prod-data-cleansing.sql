-- vervang irritante enkel quote in de naam van een programmeertaal
update project
set languages = replace(languages, 'Cap''n', 'Capn')
where languages like '%Cap%';

-- vervang enkele quotes binnen de json string met languages
update project
set languages = replace(languages,'''', '"' )
;

----------------------------
-- schoon commitinfo
-----------------------------
-- stap 1: create view om te weten wat geschoond moet worden.
CREATE MATERIALIZED VIEW IF NOT EXISTS prod.commit_met_inhoud
TABLESPACE pg_default
AS
 SELECT DISTINCT b.idcommit
   FROM prod.bestandswijziging b
  ORDER BY b.idcommit
WITH DATA;

ALTER TABLE IF EXISTS prod.commit_met_inhoud
    OWNER TO postgres;


CREATE UNIQUE INDEX idx_commit_met_inhoud_pk
    ON prod.commit_met_inhoud USING btree
    (idcommit)
    TABLESPACE pg_default;


-- stap 2
-- controle hoeveel rijen hebben we?
-- het verschil wordt geschoond
select count(*) from commit_met_inhoud; -- 86790
select count(*) from commitinfo c;      -- 131518

select count(id) from commitinfo c
where c.id not in
( select v.idcommit from commit_met_inhoud v); -- 44728

-- stap 3 opschonen.
delete from commitinfo c
where c.id not in
( select v.idcommit from commit_met_inhoud v); -- 44728