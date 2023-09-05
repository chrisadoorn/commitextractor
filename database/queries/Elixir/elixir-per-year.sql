set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen
(
    idbestandswijziging           integer           NOT NULL
);

truncate table bw_met_zoektermen;

insert into bw_met_zoektermen(idbestandswijziging)
select distinct idbestandswijziging from bestandswijziging_zoekterm
where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;


CREATE TEMPORARY TABLE IF NOT EXISTS periods
(
    start_date               date,
    end_date                date
);
truncate table periods;

insert into periods(start_date, end_date) values ('2011-12-31', '2013-01-01');
insert into periods(start_date, end_date) values ('2012-12-31', '2014-01-01');
insert into periods(start_date, end_date) values ('2013-12-31', '2015-01-01');
insert into periods(start_date, end_date) values ('2014-12-31', '2016-01-01');
insert into periods(start_date, end_date) values ('2015-12-31', '2017-01-01');
insert into periods(start_date, end_date) values ('2016-12-31', '2018-01-01');
insert into periods(start_date, end_date) values ('2017-12-31', '2019-01-01');
insert into periods(start_date, end_date) values ('2018-12-31', '2020-01-01');
insert into periods(start_date, end_date) values ('2019-12-31', '2021-01-01');
insert into periods(start_date, end_date) values ('2020-12-31', '2022-01-01');
insert into periods(start_date, end_date) values ('2021-12-31', '2023-01-01');
insert into periods(start_date, end_date) values ('2022-12-31', '2024-01-01');


CREATE TEMPORARY TABLE IF NOT EXISTS elixir_per_year
(
    year                integer,
    total               integer,
    mc                  integer,
    no_mc               integer,
    mc_perc             numeric,
    no_mc_perc          numeric,
    mc_perc_conf        numeric
);

truncate table elixir_per_year;

DO $$DECLARE r record;
BEGIN
    FOR r IN SELECT start_date, end_date FROM periods
        LOOP
            insert into elixir_per_year(year, total, mc, no_mc, mc_perc, no_mc_perc, mc_perc_conf)
            select
                extract('Year' from r.start_date) + 1,
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
                       where ci.commitdatumtijd > r.start_date and ci.commitdatumtijd < r.end_date
                         and ci.author_id is not null
                       group by authorid
                       order by nr_bestandswijzigingen_with_mc desc) as xxx) as aggregated;
        END LOOP;
END$$;




select * from elixir_per_year;