
-- aantal programmeurs per project
select count(distinct author_id) as aantal_programmeurs, idproject  
from commitinfo
group by  idproject  ;

-- aantal commits per programmeur per project 
select c.author_id,  count( p.naam),  p.naam 
from commitinfo c
    ,project p
where c.idproject = p.id
group by author_id,  p.naam 
order by author_id,  p.naam;

-- aantal projecten waaraan een programmeur gewerkt heeft;
select c.author_id, count(distinct p.naam)   
from commitinfo c
    ,project p
where c.idproject = p.id
group by  c.author_id
order by 2 desc;


-- zoek naar aantal onbekende auteurs. 
select count(distinct c.author_id)
from commitinfo c 
where author_id > 90000000

-- zoek naar aantal commits van onbekende auteurs
select count(c.author_id)
from commitinfo c 
where author_id >= 90000000;

-- 5602 programmeurs
-- 3694 bekend   = 66%   142383 commits  68%
-- 1908 onbekend = 34%    45337 commits  32%

-- spreiding door de jaren heen?
select date_part('year', commitdatumtijd) as jaar, count(date_part('year', commitdatumtijd)) as aantal
from commitinfo c2 
where author_id >= 90000000
group by date_part('year', commitdatumtijd)
order by 1 asc;

-- auteur 49699333 werkte aan 82 projecten!
--        27856297 aan 13 projecten
--        124075   aan 6 
select concat('https://www.github.com/', p.naam, '/commit/', c.hashvalue ) 
from commitinfo c 
    ,project p 
where c.idproject = p.id 
and c.author_id = 124075
limit 1;
--https://www.github.com/spotify/dbeam/commit/e6abcd19760d9801b14e975bd75295ad757c925a
-- 49699333 is van dependabot[bot]
-- 27856297 is van dependabot-preview[bot]
-- 124075   is van https://github.com/dsyer (Dave Syer) Een echt mens