set schema 'v11';

CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen_met_term
(
    idbestandswijziging           integer           NOT NULL,
    zoekterm                      varchar(255)      NOT NULL
);

truncate table bw_met_zoektermen_met_term;
insert into bw_met_zoektermen_met_term(idbestandswijziging, zoekterm)
select idbestandswijziging, zoekterm  from bestandswijziging_zoekterm where aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;


CREATE TEMPORARY TABLE IF NOT EXISTS zoektermen_tellingen
(
    zoekterm                      varchar(255),
    aantalgevonden                integer,
    percentage                    decimal(4,1),
    stddev                        decimal(4,1)

);
truncate table zoektermen_tellingen;


insert into zoektermen_tellingen(zoekterm, aantalgevonden)
select zoekterm,count(distinct ci.author_id) cnt
     from bw_met_zoektermen_met_term bzztmt
              join bestandswijziging bw on bzztmt.idbestandswijziging = bw.id
              join commitinfo ci  on ci.id = bw.idcommit
     group by zoekterm;

insert into zoektermen_tellingen(zoekterm, aantalgevonden)
select 'total' ,count(distinct ci.author_id) cnt
from bw_met_zoektermen_met_term bzztmt
         join bestandswijziging bw on bzztmt.idbestandswijziging = bw.id
         join commitinfo ci  on ci.id = bw.idcommit;

update zoektermen_tellingen
set percentage = round(100.0 * aantalgevonden / (select aantalgevonden from zoektermen_tellingen where zoekterm = 'total'),1);

update zoektermen_tellingen
set stddev = round(1.96 * sqrt( percentage  * (100 - percentage)  / (select aantalgevonden from zoektermen_tellingen where zoekterm = 'total')),1);


select * from zoektermen_tellingen order by aantalgevonden desc;



