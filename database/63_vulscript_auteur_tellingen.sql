
-- gooi eerst alles weer leeg.
truncate table auteur_tellingen;

-- voer alle combinaties auteur - project op.
insert into auteur_tellingen(auteur, project, projectid)
select distinct auteur, project, projectid
from wijziging_lineage
where auteur is not null; 


-- update met tellingen
-- totaal aantallen bestandswijzingen per auteur per project
update auteur_tellingen as qw
set aantal_totaal = (select count(distinct(bestandswijziging))
	from wijziging_lineage wl
	where qw.auteur = wl.auteur
	and qw.projectid = wl.projectid
	and wl.uitgesloten = false
) ;


-- aantallen mogelijke bestandswijzingen met multi-core statements per auteur per project
update auteur_tellingen as qw
set aantal_kandidaat = (select count(distinct(wl.bestandswijziging))
	from wijziging_lineage wl
	where qw.auteur = wl.auteur
	and qw.projectid = wl.projectid
	and wl.zoekterm is not null
	and wl.uitgesloten = false
) ;


-- aantallen andere commits per auteur per project
update auteur_tellingen as qw
set aantal_bevestigd = (select count(distinct(wl.bestandswijziging))
	from wijziging_lineage wl,
	     bestandswijziging_zoekterm bwz
	where qw.auteur = wl.auteur
	and qw.projectid = wl.projectid
	and wl.bestandswijziging = bwz.idbestandswijziging
	and wl.zoekterm = bwz.zoekterm
	and bwz.falsepositive = false
	and wl.uitgesloten = false
) ;

