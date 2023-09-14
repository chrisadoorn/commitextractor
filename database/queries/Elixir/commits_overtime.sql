
set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen_met_term
(
    idbestandswijziging           integer           NOT NULL,
    zoekterm                      varchar(255)      NOT NULL
);

truncate table bw_met_zoektermen_met_term;
insert into bw_met_zoektermen_met_term(idbestandswijziging, zoekterm)
select idbestandswijziging, zoekterm  from bestandswijziging_zoekterm where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;

select ci.id, ci.idproject, ci.commitdatumtijd,  ci.author_id,count(distinct bwz.idbestandswijziging) from commitinfo ci
left join bestandswijziging bw on ci.id = bw.idcommit
left join bw_met_zoektermen_met_term bwz on bw.id = bwz.idbestandswijziging
group by ci.id
order by ci.idproject;
