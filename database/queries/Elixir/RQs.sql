--SQ To what extent do programmers use multi-core programming
--SQ.1 How is the usage of multi-core programming primitives distributed among programmers?
--SQ.2 What is the correlation between multi-core programming primitives and the percentage of programmers using them?
--SQ.3 How has the usage of multi-core programming primitives changed over time? Is there a trend?


--SQ.1

-- aantal projecten
-- tellingen auteurs, aantal commits, aantal projecten, aantal bestandswijzigingen
set schema 'v11';
select ci.author_id authorid, count(distinct ci.id) commitid, count(distinct ci.idproject) projectid,count(distinct bw.id) bwid from commitinfo ci
left join bestandswijziging bw on ci.id = bw.idcommit
group by authorid order by authorid;


-- tellingen auteurs, aantal commits, aantal projecten, aantal bestandswijzigingen, aantal bestandswijzigingen met zoektermen gevonden
set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen
(
    idbestandswijziging           integer           NOT NULL
);

truncate table bw_met_zoektermen;

insert into bw_met_zoektermen(idbestandswijziging)
select distinct idbestandswijziging from bestandswijziging_zoekterm where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;

select ci.author_id authorid, count(distinct ci.id) commitid, count(distinct ci.idproject) projectid,count(distinct bw.id) bwid, count(distinct bwz.idbestandswijziging) with_mc  from commitinfo ci
left join bestandswijziging bw on ci.id = bw.idcommit
left join bw_met_zoektermen bwz on bw.id = bwz.idbestandswijziging
group by authorid order by with_mc;
---

set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen
(
    idbestandswijziging           integer           NOT NULL
);

truncate table bw_met_zoektermen;

insert into bw_met_zoektermen(idbestandswijziging)
select distinct idbestandswijziging from bestandswijziging_zoekterm where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;


select ci.author_id authorid, count(distinct ci.id) commitid, count(distinct ci.idproject) projectid,count(distinct bw.id) bwid, count(distinct bwz.idbestandswijziging) with_mc  from commitinfo ci
left join bestandswijziging bw on ci.id = bw.idcommit
left join bw_met_zoektermen bwz on bw.id = bwz.idbestandswijziging
where ci.author_id < 900000000
group by authorid order by with_mc;

--

set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen
(
    idbestandswijziging           integer           NOT NULL
);

truncate table bw_met_zoektermen;

insert into bw_met_zoektermen(idbestandswijziging)
select distinct idbestandswijziging from bestandswijziging_zoekterm where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;


select ci.author_id authorid, count(distinct ci.id) commitid, count(distinct ci.idproject) projectid,count(distinct bw.id) bwid, count(distinct bwz.idbestandswijziging) with_mc  from commitinfo ci
                                                                                                                                                                                           left join bestandswijziging bw on ci.id = bw.idcommit
                                                                                                                                                                                           left join bw_met_zoektermen bwz on bw.id = bwz.idbestandswijziging
where ci.author_id >= 900000000
group by authorid order by with_mc;
 ---

projecten met mc
percentage auteurs met mc

set schema 'v11';

CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen_met_term
(
    idbestandswijziging           integer           NOT NULL,
    zoekterm                      varchar(255)      NOT NULL
);

truncate table bw_met_zoektermen_met_term;
insert into bw_met_zoektermen_met_term(idbestandswijziging, zoekterm)
select idbestandswijziging, zoekterm  from bestandswijziging_zoekterm where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;


select pr.id, pr.naam, author_id, count(distinct bzztmt.zoekterm) from project pr
left join commitinfo ci on ci.idproject = pr.id
left join bw_met_zoektermen_met_term bzztmt on bzztmt.idbestandswijziging = ci.id
group by pr.id, ci.author_id
         order by pr.id;


select xxx.id, xxx.aantal_commits,xxx.naam, count(xxx.author_id), count(xxx.cc)filter(where xxx.cc = 0) nr_no_mc, count(xxx.cc)filter(where xxx.cc > 0) nr_mc from
(select pr.id, pr.aantal_commits, pr.naam, author_id, count(distinct bzztmt.zoekterm) as cc from project pr
left join commitinfo ci on ci.idproject = pr.id
left join bw_met_zoektermen_met_term bzztmt on bzztmt.idbestandswijziging = ci.id
group by pr.id, ci.author_id) as xxx
group by id, aantal_commits, naam
order by id;
















-- aantal auteurs gevonden in


select count(distinct ci.author_id) filter(where ci.author_id < 900000000) , count(distinct ci.author_id) filter(where ci.author_id >= 900000000) from commitinfo ci

--SQ.2 What is the correlation between multi-core programming primitives and the percentage of programmers using them?

set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen_met_term
(
    idbestandswijziging           integer           NOT NULL,
    zoekterm                      varchar(255)      NOT NULL
);

truncate table bw_met_zoektermen_met_term;
insert into bw_met_zoektermen_met_term(idbestandswijziging, zoekterm)
select idbestandswijziging, zoekterm  from bestandswijziging_zoekterm where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;

select zoekterm, count(idbestandswijziging) from bw_met_zoektermen_met_term
group by zoekterm;

select
zoekterm, count(distinct ci.author_id)
from bw_met_zoektermen_met_term bzztmt
join bestandswijziging bw on bzztmt.idbestandswijziging = bw.id
join commitinfo ci  on ci.id = bw.idcommit
group by zoekterm
order by  zoekterm

