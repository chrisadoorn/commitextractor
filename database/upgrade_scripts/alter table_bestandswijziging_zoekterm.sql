alter table bestandswijziging_zoekterm ADD CONSTRAINT bestandswijziging_ak unique (idbestandswijziging, zoekterm); 
CREATE INDEX bestandswijziging_zoekterm_ak_idx ON bestandswijziging_zoekterm (idbestandswijziging, zoekterm);

-- Voer hierna eerst het script 44_create_table_bestandswijziging_zoekterm_regelnummer.sql uit
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
where aantalgevonden_nieuw != aantalgevonden;

-- kopieer aantalgevonden -> aantalgevonden_oud
update bestandswijziging_zoekterm
set aantalgevonden_nieuw = aantalgevonden;

-- controle achteraf: resultaat moet 0 zijn
select count(*) from bestandswijziging_zoekterm
where aantalgevonden_nieuw != aantalgevonden;

-- kopieer bestaande regelnummers naar bzr tabel.
insert into bestandswijziging_zoekterm_regelnummer 
(idbestandswijziging, zoekterm, regelnummer, regelsoort)
select idbestandswijziging, zoekterm, unnest (regelnummers) as regelnummer, 'nieuw' from bestandswijziging_zoekterm; 

-- verwijder kolommen regelnummers, aantal_gevonden
alter table bestandswijziging_zoekterm 
drop column regelnummers,
drop column aantalgevonden;

-- all done
