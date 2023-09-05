
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



select count(distinct a.id) ta , count(distinct a.id) filter (where is_mc = true ) t_mc, count(distinct a.id) filter (where is_mc = false ) t_nmc
     , count(bw.id) fc, count(bw.id)filter (where is_mc = true ) fc_mc, count(bw.id)filter (where is_mc = false ) fc_nmc  from authors a
join commitinfo ci on a.id = ci.author_id
join bestandswijziging bw on ci.id = bw.idcommit

union

select 0,0,0,round(fc/(1.0*ta),1) as programmer, round(fc_mc/(1.0*t_mc),1) as MC_programmer , round(fc_nmc/(1.0*t_nmc),1) as non_MC_programmer from
    (select count(distinct a.id) ta , count(distinct a.id) filter (where is_mc = true ) t_mc, count(distinct a.id) filter (where is_mc = false ) t_nmc
   , count(bw.id) fc, count(bw.id)filter (where is_mc = true ) fc_mc, count(bw.id)filter (where is_mc = false ) fc_nmc  from authors a
join commitinfo ci on a.id = ci.author_id
join bestandswijziging bw on ci.id = bw.idcommit) as xxx

union

select 0,0,0,0,nr_a, round(nr_wijzgingen/(1.0*nr_a), 1) from
(select count(distinct a.id) nr_a,  count(distinct idbestandswijziging) nr_wijzgingen from authors a
join commitinfo ci on a.id = ci.author_id
join bestandswijziging bw on ci.id = bw.idcommit
left join v11.bestandswijziging_zoekterm bwz on bw.id = bwz.idbestandswijziging
where a.is_mc = true and bwz.falsepositive = false and bwz.aantalgevonden_nieuw > bwz.aantalgevonden_oud) as zzz







--    select count(distinct bw.id) from bestandswijziging bw
--    left join v11.bestandswijziging_zoekterm bwz on bw.id = bwz.idbestandswijziging
--   where bwz.falsepositive = false and bwz.aantalgevonden_nieuw > bwz.aantalgevonden_oud










