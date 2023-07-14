----------------------------
-- schoon commitinfo
-----------------------------
-- stap 1: create table om te weten wat geschoond moet worden.
CREATE TABLE id_in_use (
	idcommit int8 NOT NULL
);

truncate table id_in_use;

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
-- het verschil wordt geschoond          --  PRD1
select count(*) from id_in_use;         -- 303330 
select count(*) from commitinfo c;      -- 602573

select count(id) from commitinfo c
where c.id not in
( select v.idcommit from id_in_use v);  -- 299243

-- stap 3 opschonen.
delete from commitinfo c
where c.id not in
( select v.idcommit from id_in_use v);   -- 37418

-- stap 4 opruimen

	drop table id_in_use;

-- tel hoeveel projecten er wijzigingen hebben
select count( distinct projectid )
from wijziging_lineage wl; -- 1078

-- tel hoeveel er geen wijzigingen hebben
-- 17 eerder fout gegaan.
select * from project p 
where idselectie = 1
--and id not in ( select distinct projectid from wijziging_lineage wl2)          -- alleen deze: 21 zonder bestandswijzigingen
and id in (select id from verwerk_project vp where resultaat = 'mislukt'); -- alleen deze: 17 eerder gefaald 
                                                                           --  not & in: 12 zonder bestandswijzigingen ( nooit gestart )
                                                                           --  in  & in: 5 met bestandswijzigingen. (halfweg gefaald)

                                                                           --  not  & not: 9 zonder bestandswijzigingen, niet gefaald 