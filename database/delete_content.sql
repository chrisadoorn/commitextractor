set schema 'test';

--voor load projecten
delete from  test.selectie;
delete from  test.project;

--na load projecten
delete from  test.verwerk_project;
delete from  test.verwerking_geschiedenis;
delete from  test.processor;
delete from  test.bestandswijziging_zoekterm;
delete from  test.bestandswijziging_info;
delete from  test.bestandswijziging;
delete from  test.commitinfo;

