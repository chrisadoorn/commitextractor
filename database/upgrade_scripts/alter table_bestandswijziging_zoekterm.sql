-- Voer eerst het script 44_create_table_bestandswijziging_zoekterm_regelnummer.sql uit
-- aan het eind van dit script wordt de data gemigreerd naar de tabel die in dat script is aangemaakt.

-- nieuwe kolommen
alter table bestandswijziging_zoekterm 
add   afkeurreden character varying NULL,
add   aantalgevonden_oud integer DEFAULT 0,
add   aantalgevonden_nieuw integer DEFAULT 0;

-- controle vooraf: de twee getallen moeten gelijk zijn
select count(*) from bestandswijziging_zoekterm
where aantalgevonden > 0;
select count(*) from bestandswijziging_zoekterm
where aantalgevonden_oud != aantalgevonden;

-- kopieer aantalgevonden -> aantalgevonden_oud
update bestandswijziging_zoekterm
set aantalgevonden_oud = aantalgevonden_oud;

-- controle achteraf: resultaat moet 0 zijn
select count(*) from bestandswijziging_zoekterm
where aantalgevonden_oud != aantalgevonden_oud;

-- kopieer bestaande regelnummers naar bzr tabel.
insert into bestandswijziging_zoekterm_regelnummer 
(idbestandswijzigingzoekterm, regelnummer, regelsoort)
select id, unnest (regelnummers) as regelnummer, 'oud' from bestandswijziging_zoekterm; 

-- verwijder kolommen regelnummers, aantal_gevonden
alter table bestandswijziging_zoekterm 
drop column regelnummers,
drop column aantalgevonden;

-- all done
