CREATE TEMPORARY TABLE IF NOT EXISTS auteur_tellingen
(
    auteur           integer           NOT NULL,
    project          character varying not null,
    projectid        integer           not null,
    aantal_kandidaat integer default 0,
    aantal_bevestigd integer default 0,
    aantal_totaal    integer default 0,
    CONSTRAINT auteur_tellingen_uk UNIQUE (auteur, projectid)
);

truncate table auteur_tellingen;

insert into auteur_tellingen(auteur, project, projectid)
select distinct auteur, project, projectid
from wijziging_lineage
where auteur is not null;


update auteur_tellingen as qw
set aantal_totaal = subquery.aantal_totaal
from (select auteur, projectid, count(distinct(bestandswijziging)) aantal_totaal
      from wijziging_lineage
      group by auteur, projectid) as subquery
where qw.auteur = subquery.auteur
  and qw.projectid = subquery.projectid;


-- aantallen mogelijke bestandswijzingen met multi-core statements per auteur per project
update auteur_tellingen as qw
set aantal_kandidaat = subquery.aantal_totaal
from (select auteur, projectid, count(distinct(wl.bestandswijziging)) aantal_totaal
      from wijziging_lineage wl
      where wl.zoekterm is not null
      group by auteur, projectid) as subquery
where qw.auteur = subquery.auteur
  and qw.projectid = subquery.projectid;


-- aantallen andere commits per auteur per project
update auteur_tellingen as qw
set aantal_bevestigd = subquery.aantal_totaal
from (select wl.auteur, wl.projectid, count(distinct(wl.bestandswijziging)) as aantal_totaal
      from wijziging_lineage wl,
           bestandswijziging_zoekterm bwz
      where wl.bestandswijziging = bwz.idbestandswijziging
        and wl.zoekterm = bwz.zoekterm
        and bwz.falsepositive = false
      group by auteur, projectid) as subquery
where qw.auteur = subquery.auteur
  and qw.projectid = subquery.projectid;

CREATE TEMPORARY TABLE IF NOT EXISTS SQ1_compare
(
    projectid         integer           not null,
    projectnaam       character varying not null,
    unieke_auteurs    integer           not null,
    unieke_MC_auteurs integer default 0,
    comparatio        float   default 0
);

truncate table SQ1_compare;

-- projecten en unieke auteurs
insert into SQ1_compare(projectid, projectnaam, unieke_auteurs)
select a.id, a.naam, count(distinct (b.author_id))
from project a
 join commitinfo b on a.id = b.idproject
 join bestandswijziging b2 on b.id = b2.idcommit
group by a.id, a.naam order by a.naam;

-- update met tellingen
-- -- projecten en unieke MC-auteurs
update SQ1_compare as sq1
set unieke_MC_auteurs =  subquery.total
from
    (select a.id as projectid, count(distinct(b.author_id)) total
                         from project a,
                              commitinfo b,
                              bestandswijziging c,
                              bestandswijziging_zoekterm d
                         where a.id = b.idproject
                           and b.id = c.idcommit
                           and c.id = d.idbestandswijziging
                         and d.falsepositive = false
     group by projectid

                         ) as subquery
where sq1.projectid = subquery.projectid;

--comparatio auteurs/MC auteurs
update SQ1_compare
set comparatio = (cast(unieke_MC_auteurs AS DECIMAL) / unieke_auteurs) * 100
where unieke_auteurs > 0;

-- toevoegen totaalregel
insert into SQ1_compare(projectid, projectnaam, unieke_auteurs)
values (0, 'totaal', 0);

update SQ1_compare
set unieke_auteurs = (select count(distinct author_id) from commitinfo)
where projectid = 0;

update SQ1_compare
set unieke_MC_auteurs = (select count(distinct auteur)
                         from auteur_tellingen
                         where aantal_bevestigd > 0)
where projectid = 0;

update SQ1_compare
set comparatio = (cast(unieke_MC_auteurs AS DECIMAL) / unieke_auteurs) * 100
where projectid = 0;

select * from SQ1_compare order by projectnaam;
select * from auteur_tellingen;

