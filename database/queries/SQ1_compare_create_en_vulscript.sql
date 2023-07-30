CREATE TABLE IF NOT EXISTS SQ1_compare
(
    projectid integer not null,
    projectnaam   character varying not null,
    unieke_auteurs integer not null,
    unieke_MC_auteurs  integer default 0,
    comparatio float default 0
)
TABLESPACE pg_default;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE auteur_tellingen TO appl;

COMMENT ON TABLE auteur_tellingen
    IS 'SQ1: How is the usage of multi-core programming primitives distributed among programmers? Table for comparison between authors and MC-authors in a project'
    ;

   -- gooi eerst alles weer leeg.
truncate table SQ1_compare;

-- projecten en unieke auteurs
insert into SQ1_compare(projectid, projectnaam, unieke_auteurs)
select a.id, a.naam, count(distinct(b.author_id))
from project a,
     commitinfo b
where a.id = b.idproject
group by a.id, a.naam;

-- update met tellingen
-- projecten en unieke MC-auteurs
update SQ1_compare as sq1
set unieke_MC_auteurs = (select count(distinct(b.author_id))
	from project a,
     commitinfo b,
     bestandswijziging c,
     bestandswijziging_zoekterm d
	where a.id = sq1.projectid
	    and a.id = b.idproject
        and b.id = c.idcommit
        and c.id = d.idbestandswijziging
) ;

--comparatio auteurs/MC auteurs
update SQ1_compare 
set comparatio = (cast(unieke_MC_auteurs AS DECIMAL)/unieke_auteurs) * 100
where unieke_auteurs > 0; 

-- toevoegen totaalregel 
insert into SQ1_compare(projectid, projectnaam, unieke_auteurs)
values(0, 'totaal', 0);
update SQ1_compare set unieke_auteurs = (select count(distinct author_id) from commitinfo)
where projectid = 0;
update  SQ1_compare set unieke_MC_auteurs = (select count(distinct auteur)from auteur_tellingen
where aantal_bevestigd > 0)
where projectid = 0;
update SQ1_compare 
set comparatio = (cast(unieke_MC_auteurs AS DECIMAL)/unieke_auteurs) * 100
where projectid = 0; 




