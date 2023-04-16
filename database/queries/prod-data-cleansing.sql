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
-- stap 1: create table om te weten wat geschoond moet worden.
CREATE TABLE id_in_use (
	idcommit int8 NOT NULL
);

-- Permissions

ALTER TABLE id_in_use OWNER TO postgres;
GRANT ALL ON TABLE id_in_use TO postgres;

insert into id_in_use(idcommit)
SELECT DISTINCT b.idcommit
   FROM bestandswijziging b;

CREATE UNIQUE INDEX idx_bestandswijzging_idcommit
    ON id_in_use USING btree
    (idcommit ASC NULLS LAST)
;

ALTER TABLE IF EXISTS id_in_use
    CLUSTER ON idx_bestandswijzging_idcommit;


-- stap 2
-- controle hoeveel rijen hebben we?
-- het verschil wordt geschoond
select count(*) from id_in_use; -- 86790
select count(*) from commitinfo c;      -- 131518

select count(id) from commitinfo c
where c.id not in
( select v.idcommit from id_in_use v); -- 44728

-- stap 3 opschonen.
delete from commitinfo c
where c.id not in
( select v.idcommit from id_in_use v); -- 44728

-- stap 4 opruimen

	drop table id_in_use;

