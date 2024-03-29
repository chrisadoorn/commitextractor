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



select count(xxx.authorid),
       count(xxx.with_mc) filter(where xxx.with_mc > 0) as nr_mc, count(xxx.with_mc) filter(where xxx.with_mc = 0) as nr_no_mc
    from
(select ci.author_id authorid,
       count(distinct ci.id) nr_commits,
       count(distinct ci.idproject) nr_projects,
       count(distinct bw.id) nr_bestands_wijzigingen,
       count(distinct bwz.idbestandswijziging) with_mc
from commitinfo ci
         left join bestandswijziging bw on ci.id = bw.idcommit
         left join bw_met_zoektermen bwz on bw.id = bwz.idbestandswijziging
where ci.commitdatumtijd >= '2023-01-01' and ci.commitdatumtijd < '2024-01-01'
group by authorid) as xxx;


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


---
set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen
(
    idbestandswijziging           integer           NOT NULL
);

truncate table bw_met_zoektermen;

insert into bw_met_zoektermen(idbestandswijziging)
select distinct idbestandswijziging from bestandswijziging_zoekterm where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;




select xxx.id, xxx.aantal_commits,xxx.naam, count(xxx.author_id) as total_p,
       count(xxx.author_id)filter(where xxx.cc = 0) as nr_no_mc,
       count(xxx.author_id)filter(where xxx.cc > 0) as nr_mc,
       count(xxx.author_id)filter(where xxx.cc > 0)/count(xxx.author_id)::float*100 as perc_mc
from
(select pr.id, pr.aantal_commits, pr.naam, author_id, count(distinct bzztmt.idbestandswijziging) as cc from project pr
left join commitinfo ci on ci.idproject = pr.id
left join bestandswijziging bw on ci.id = bw.idcommit
left join bw_met_zoektermen bzztmt on bzztmt.idbestandswijziging = bw.id
group by pr.id, ci.author_id) as xxx
group by id, aantal_commits, naam
order by id;



---


select pr.id, pr.naam, author_id,count(distinct bzztmt.idbestandswijziging) from project pr
left join commitinfo ci on ci.idproject = pr.id
left join bestandswijziging bw on ci.id = bw.idcommit
left join bw_met_zoektermen bzztmt on bzztmt.idbestandswijziging = bw.id
group by pr.id, ci.author_id
order by pr.id;

select pr.id, pr.aantal_commits, pr.naam, author_id, count(distinct bzztmt.idbestandswijziging) as cc from project pr
left join commitinfo ci on ci.idproject = pr.id
left join bestandswijziging bw on ci.id = bw.idcommit
left join bw_met_zoektermen bzztmt on bzztmt.idbestandswijziging = bw.id
group by pr.id, ci.author_id;









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

select zoekterm, count(distinct ci.author_id)
from bw_met_zoektermen_met_term bzztmt
join bestandswijziging bw on bzztmt.idbestandswijziging = bw.id
join commitinfo ci  on ci.id = bw.idcommit
group by zoekterm
order by  zoekterm;


--SQ.3 How has the usage of multi-core programming primitives changed over time? Is there a trend?

select ci.id, ci.idproject, ci.commitdatumtijd,  ci.author_id,count(distinct bwz.idbestandswijziging) from commitinfo ci
left join bestandswijziging bw on ci.id = bw.idcommit
left join bw_met_zoektermen bwz on bw.id = bwz.idbestandswijziging
group by ci.id
order by idproject;

SELECT date_trunc('month', commitdatumtijd) AS txn_month, count(*), count(*) filter(where count = 0)
    ,count(*) filter(where count > 0), count(*) filter(where count > 0)/count(*)::float*100 as perc
FROM v11."Result_20_commits_date"
GROUP BY txn_month order by txn_month ;



---
--experimenten

select * from bw_met_zoektermen_met_term;


-- count number of primitives used by mc programmars
select xxx.cnt, count(xxx.cnt) as c , round(100*count(xxx.cnt)/3547.0,1)as perc, round(100 * 1.96 * sqrt( count(xxx.cnt)/3547.0  * (1 - count(xxx.cnt)/3547.0) / 3547),1)  from
(select count(distinct bwzt.zoekterm) as cnt from commitinfo ci
left join bestandswijziging bw on ci.id = bw.idcommit
left join bw_met_zoektermen_met_term bwzt on bw.id = bwzt.idbestandswijziging
group by ci.author_id) as xxx
where xxx.cnt > 0
group by xxx.cnt;


-- number of file changes

set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS authors
(
    id           integer           NOT NULL,
    is_mc        boolean           NOT NULL
);

truncate table authors;

insert into authors(id, is_mc)
select xxx.author_id as id, case when xxx.is_mc > 0 then true else false end as is_mc from
(select ci.author_id,count(bwz.zoekterm) filter(where bwz.falsepositive = false and bwz.aantalgevonden_nieuw > bwz.aantalgevonden_oud ) as is_mc from commitinfo ci
join v11.bestandswijziging bw on ci.id = bw.idcommit
left join v11.bestandswijziging_zoekterm bwz on bw.id = bwz.idbestandswijziging
group by ci.author_id
order by ci.author_id) as xxx;


select a.id, a.is_mc, count(b.id), count(b.id) filter ( where a.is_mc = true ), count(b.id) filter ( where a.is_mc = false ) from authors as a
join commitinfo ci on a.id = ci.author_id
join v11.bestandswijziging b on ci.id = b.idcommit
group by a.id,a.is_mc


select p.id, p.naam, count(*) from project p
join commitinfo ci on p.id = ci.idproject
join bestandswijziging bw on ci.id = bw.idcommit
join bestandswijziging_zoekterm bwz on bw.id = bwz.idbestandswijziging
where bwz.falsepositive = false and bwz.aantalgevonden_nieuw > bwz.aantalgevonden_oud
group by p.id


3
