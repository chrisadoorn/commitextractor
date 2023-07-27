----------------------------
-- schoon bestandswijziging, projecten waarbij de extractie mislukt is, en die niet verder verwerkt worden.
---------------------------
-- tellen
select count(*)
from bestandswijziging b 
where idcommit in (select id
from commitinfo c 
where idproject 
in ( select id from verwerk_project vp
     where processtap = 'extractie'
     and resultaat = 'mislukt' ));
-- verwijderen
delete 
from bestandswijziging b 
where idcommit in (select id
from commitinfo c 
where idproject 
in ( select id from verwerk_project vp
     where processtap = 'extractie'
     and resultaat = 'mislukt' ));



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
select count(*) from id_in_use;         -- 256759 --> 335060
select count(*) from commitinfo c;      -- 602573 --> 460125

select count(id) from commitinfo c
where c.id not in
( select v.idcommit from id_in_use v);  -- 345814 --> 125065

-- stap 3 opschonen.
delete from commitinfo c
where c.id not in
( select v.idcommit from id_in_use v);   -- 37418 --> 125065

-- stap 4 opruimen

	drop table id_in_use;

-- tel hoeveel projecten er wijzigingen hebben
select count( distinct projectid )
from wijziging_lineage wl; -- 1090
9 projecten zonder java code in .java files (wel in .pde, .md, ...  files)


-- tel hoeveel er geen wijzigingen hebben
-- 17 eerder fout gegaan.
select * from project p 
where idselectie = 1
and id not in ( select distinct projectid from wijziging_lineage wl2)          -- alleen deze: 9 zonder bestandswijzigingen
                                                                           --  not  & not: 9 zonder bestandswijzigingen, niet gefaald 