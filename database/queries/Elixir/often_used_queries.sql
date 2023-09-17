set schema 'v11';

-- Reset voor text_searcher
update v11.verwerk_project set processtap = ' ', resultaat = 'verwerkt', start_verwerking = null, einde_verwerking = null;

delete from v11.bestandswijziging_info;
delete from v11.bestandswijziging_zoekterm;
delete from v11.bestandswijziging_zoekterm_regelnummer;

