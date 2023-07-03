
-- gooi eerst alles weer leeg.
truncate table auteur_tellingen;

-- voer alle combinaties auteur - project op.
insert into auteur_tellingen(auteur, project, projectid)
select distinct auteur, project, projectid
from wijziging_lineage
where auteur is not null; -- 1596


-- update met tellingen
-- totaal aantallen commits per auteur per project 
update auteur_tellingen as qw
set aantal_totaal = (select count(wl.auteur)
	from wijziging_lineage wl
	where qw.auteur = wl.auteur 
	and qw.projectid = wl.projectid 
) ;


-- aantallen multi-core commits per auteur per project 
update auteur_tellingen as qw
set aantal_mc = (select count(wl.auteur)
	from wijziging_lineage wl
	where qw.auteur = wl.auteur 
	and qw.projectid = wl.projectid 
	and wl.zoekterm is not null
) ;


-- aantallen andere commits per auteur per project 
update auteur_tellingen as qw
set aantal_not_mc = (select count(wl.auteur)
	from wijziging_lineage wl
	where qw.auteur = wl.auteur
	and qw.projectid = wl.projectid 
	and wl.zoekterm is null
) ;

