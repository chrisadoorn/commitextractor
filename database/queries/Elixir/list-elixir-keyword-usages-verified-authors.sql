set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen
(
    idbestandswijziging           integer           NOT NULL
);

truncate table bw_met_zoektermen;

insert into bw_met_zoektermen(idbestandswijziging)
select distinct idbestandswijziging from bestandswijziging_zoekterm
where aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;


select
    total,
    mc, no_mc ,
    round(100.0 * mc / total,1),
    round(100.0 *  no_mc / total,1),
    round(100 * 1.96 * sqrt( (1.0 * mc/total  * (1.0 - 1.0 * mc/total) )/ total),1)

from
    (select count(xxx.authorid) filter ( where xxx.nr_bestandswijzigingen_with_mc > 0 ) mc,
            count(xxx.authorid) filter ( where xxx.nr_bestandswijzigingen_with_mc = 0 ) no_mc,
            count(xxx.authorid) total
     from (select ci.author_id authorid, count(distinct bwz.idbestandswijziging) nr_bestandswijzigingen_with_mc
           from commitinfo ci
                    left join bestandswijziging bw on ci.id = bw.idcommit
                    left join bw_met_zoektermen bwz on bw.id = bwz.idbestandswijziging
           where ci.author_id < 900000000
           group by authorid
           order by nr_bestandswijzigingen_with_mc desc) as xxx) as aggregated
