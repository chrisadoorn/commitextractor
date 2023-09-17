update v11.bestandswijziging_zoekterm bwz set aantalgevonden_oud =
( select count(rn.id) from v11.bestandswijziging_zoekterm_regelnummer rn
where bwz.idbestandswijziging = rn.idbestandswijziging and rn.regelsoort = 'oud' and rn.zoekterm = bwz.zoekterm  and rn.is_valid_2 = true);


update v11.bestandswijziging_zoekterm bwz set aantalgevonden_nieuw =
( select count(rn.id) from v11.bestandswijziging_zoekterm_regelnummer rn
where bwz.idbestandswijziging = rn.idbestandswijziging and rn.regelsoort = 'nieuw' and rn.zoekterm = bwz.zoekterm and rn.is_valid_2 = true);

