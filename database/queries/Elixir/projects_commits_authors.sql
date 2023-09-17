set schema 'v11';
CREATE TEMPORARY TABLE IF NOT EXISTS bw_met_zoektermen
(
    idbestandswijziging           integer           NOT NULL
);

truncate table bw_met_zoektermen;

insert into bw_met_zoektermen(idbestandswijziging)
select distinct idbestandswijziging from bestandswijziging_zoekterm
where falsepositive = false and aantalgevonden_nieuw > bestandswijziging_zoekterm.aantalgevonden_oud;



CREATE TABLE IF NOT EXISTS projects_commits_authors
(
    project_id                     integer           NOT NULL,
    number_of_commits              integer           NOT NULL,
    project_name                   varchar           NOT NULL,
    total_projects                 integer           NOT NULL,
    nr_no_mc                       integer           NOT NULL,
    nr_mc                          integer           NOT NULL,
    perc_mc                        double precision  NOT NULL
);

truncate table projects_commits_authors;




insert into projects_commits_authors(project_id, number_of_commits, project_name, total_projects, nr_no_mc, nr_mc, perc_mc)
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