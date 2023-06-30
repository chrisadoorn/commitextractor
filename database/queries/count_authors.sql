-- alle authors
select count(distinct author_id) from commitinfo c -- 1911

-- authors die multi-core commit uitvoeren
select count(distinct author_id)                  -- 660 = 34%
from commitinfo c 
 , java_parse_result jpr 
where jpr.commit_id = c.id

-- geidentifeerde authors
select count(distinct author_id)                  -- 496 = 26% van alles
from commitinfo c                                 --     = 75% van authors die mc doen
 , java_parse_result jpr 
where jpr.commit_id = c.id
and author_id < 900000000;

-- aanpasingen in verhouding tot tijdsduur project

-- mc aanpassingen in verhouding tot andere aanpassingen
