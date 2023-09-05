set schema 'v11';


CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen_met_term
(
    idbestandswijziging           integer           NOT NULL,
    zoekterm                      varchar(255)      NOT NULL
);

truncate table bw_met_zoektermen_met_term;
insert into bw_met_zoektermen_met_term(idbestandswijziging, zoekterm)
select idbestandswijziging, zoekterm  from bestandswijziging_zoekterm where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;


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
group by a.id,a.is_mc;

CREATE TEMPORARY TABLE IF NOT EXISTS result_table
(
    cnt integer,
    c integer,
    perc numeric,
    conf numeric
);

truncate table result_table;

DO $$DECLARE r record;
BEGIN
    for r in select count(*) as c from authors where is_mc = true
    loop
            insert into result_table
            select xxx.cnt, count(xxx.cnt) as c , round(count(xxx.cnt)/(r.c/100.0),1)as perc, round(1.96 * sqrt( count(xxx.cnt)/(r.c/100.0)  * (100 - count(xxx.cnt)/(r.c/100.0)) / r.c),1)  from
                (select count(distinct bwzt.zoekterm) as cnt from commitinfo ci
            left join bestandswijziging bw on ci.id = bw.idcommit
            left join bw_met_zoektermen_met_term bwzt on bw.id = bwzt.idbestandswijziging
                 group by ci.author_id) as xxx
            where xxx.cnt > 0
            group by xxx.cnt;
    end loop;

END$$;

select * from result_table order by cnt;