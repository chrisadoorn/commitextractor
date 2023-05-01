set schema 'test';

--na load projecten
delete from  verwerk_project;
delete from  verwerking_geschiedenis;
delete from  processor;
delete from  bestandswijziging_zoekterm;
delete from  bestandswijziging_info;
delete from  bestandswijziging;
delete from  commitinfo;

--voor load projecten
delete from  project;
delete from  selectie;

