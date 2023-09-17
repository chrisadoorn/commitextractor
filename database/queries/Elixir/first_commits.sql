set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS authors
(
    id           integer           NOT NULL,
    is_mc        boolean           NOT NULL
);

truncate table authors;

insert into authors(id, is_mc)
select xxx.author_id as id, case when xxx.is_mc > 0 then true else false end as is_mc from
    (select ci.author_id, count(bwz.zoekterm) filter(where bwz.falsepositive = false and bwz.aantalgevonden_nieuw > bwz.aantalgevonden_oud ) as is_mc from commitinfo ci
     join v11.bestandswijziging bw on ci.id = bw.idcommit
     left join v11.bestandswijziging_zoekterm bwz on bw.id = bwz.idbestandswijziging
     group by ci.author_id
     order by ci.author_id) as xxx;


CREATE TABLE IF NOT EXISTS month_count_first_commit
(
    month_date   date           NOT NULL,
    first_commit_count    integer           NOT NULL
);

truncate table month_count_first_commit;

insert into month_count_first_commit(month_date, first_commit_count)
SELECT date_trunc('month', xxx.mindate) AS txn_month, count(*)
from
(select author_id, min(commitdatumtijd) mindate from authors
join commitinfo ci on authors.id = ci.author_id
group by ci.author_id
order by min(commitdatumtijd) asc) as xxx
GROUP BY txn_month order by txn_month ;