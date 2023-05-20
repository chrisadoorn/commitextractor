
-- aantal programmeurs per project
select count(distinct author_id) as aantal_programmeurs, idproject  
from commitinfo
group by  idproject;

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


-- zoek naar aantal onbekende auteurs. -- 1804 op 5602 totaal
select count(distinct c.author_id)
from commitinfo c 
where author_id > 900000000

-- zoek naar aantal commits van onbekende auteurs -- 44626 op 187720 totaal
select count(c.author_id)
from commitinfo c 
where author_id >= 900000000;

-- 5602 programmeurs totaal met 187720 commits
-- 3798 bekend   = 68%   143094 commits  76%
-- 1804 onbekend = 32%    44626 commits  24%

-- spreiding door de jaren heen?
select date_part('year', commitdatumtijd) as jaar, count(date_part('year', commitdatumtijd)) as aantal
from commitinfo c2 
where author_id >= 900000000
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


-- aantal auteurs
select c.author_id, c.username, c.emailaddress 
from commitinfo c 
where c.author_id >= 900000000; -- 1908

-- aantal usernames
select count( distinct c.username) -- 1643
from commitinfo c 
where c.author_id >= 900000000;

-- aantal emailadressen
select count( distinct c.emailaddress) -- 1732
from commitinfo c 
where c.author_id >= 900000000;

select count( distinct concat(c.username, c.emailaddress)) -- 1825
from commitinfo c 
where c.author_id >= 900000000;

SELECT count(DISTINCT concat(c.username, c.emailaddress, c.author_id))
from commitinfo c
where c.author_id >= 900000000; --1844


-- tabel voor helpen met analyse
create table author_analyse(
concatenatie_ue character varying,
concatenatie_uea character varying,
username character varying,
emailaddress character varying,
author_id int,
project_id int,
alternatief_id int
);



select count(distinct(emailaddress))
from author_analyse 

select distinct(length(emailaddress))
from author_analyse 


-- vul tabel stap 1
insert into author_analyse (concatenatie_uea)
select distinct(concat(c.username, c.emailaddress, c.author_id))
   FROM commitinfo c
where c.author_id >= 900000000;
                     
-- vul tabel stap 2
update author_analyse
set username = substring(concatenatie_uea from 1 for 64)
   ,emailaddress = substring(concatenatie_uea from 65 for 64)
   ,concatenatie_ue = substring(concatenatie_uea from 1 for 128)
   ,author_id = cast(substring(concatenatie_uea from 129 ) as integer); --  klopt!

 --controles
-- opnieuw concateneren moet zelfde waarde opleveren. Hier mag dus niets gevonden worden.   
select * 
from author_analyse aa 
where concat(aa.username, aa.emailaddress, aa.author_id) != aa.concatenatie_uea; --  klopt!

-- hier mag ook niet niets gevonden worden.   
select * 
from author_analyse aa 
where concat(aa.concatenatie_ue , aa.author_id) != aa.concatenatie_uea;  --  klopt!

-- en getallen moeten kloppen met eerder gevonden aantallen
select count(distinct(emailaddress))
from author_analyse;  -- 1732 klopt!
select count(distinct(username))
from author_analyse;  -- 1643 klopt!
select count(distinct(author_id))
from author_analyse;  --  klopt!
select count(distinct(concatenatie_ue))
from author_analyse;  --  klopt!
select count(*)
from author_analyse;  -- 1844 klopt!

-- vul tabel stap 3, vullen project_id
-- dit werkt omdat wij hebben gedefineerd dat een author per project wordt bekeken.  
update author_analyse aa
set project_id = (select distinct(c.idproject) 
                  from commitinfo c
                  where c.author_id = aa.author_id); 
                

select count(*)
from author_analyse aa 
where aa.project_id is null;

-- unieke username icm meerdere emailadressen? -- 43 regels, 16 usernames, 22 verschillende emailadressen, mogelijk tellen wij hier  teveel
select ab.username, ab.emailaddress, ab.author_id, ab.project_id
from author_analyse ab 
where ab.username in (select aa.username
from author_analyse aa
group by aa.username, aa.emailaddress
having count(aa.emailaddress) > 1)
order by ab.username ;

-- aantal usernames hierbinnen
select distinct(ab.username) as aantal_usernames
from author_analyse ab 
where ab.username in (select aa.username
from author_analyse aa
group by aa.username, aa.emailaddress
having count(aa.emailaddress) > 1);

-- aantal emailadressen hierbinnen
select distinct(ab.emailaddress) as aantal_emailadressen
from author_analyse ab 
where ab.username in (select aa.username
from author_analyse aa
group by aa.username, aa.emailaddress
having count(aa.emailaddress) > 1);

-- unieke emailadres icm meerdere usernames? -- 35 regels, 15 emailadres, 16 usernames, mogelijk tellen wij hier 1 x teveel 
select ab.username, ab.emailaddress, ab.author_id, ab.project_id
from author_analyse ab 
where ab.emailaddress in (select aa.emailaddress
from author_analyse aa
group by aa.username, aa.emailaddress
having count(aa.username) > 1)
order by ab.emailaddress ;

-- aantal usernames hierbinnen
select distinct(ab.username) as aantal_usernames
from author_analyse ab 
where ab.emailaddress in (select aa.emailaddress
from author_analyse aa
group by aa.username, aa.emailaddress
having count(aa.username) > 1);

-- aantal emailadressen hierbinnen
select distinct(ab.emailaddress) as aantal_email
from author_analyse ab 
where ab.emailaddress in (select aa.emailaddress
from author_analyse aa
group by aa.username, aa.emailaddress
having count(aa.username) > 1);

-- emailadressen van onbekende gebruikers, die voorkomen bij bekende gebruikers
select count(c.emailaddress) -- 0
from commitinfo c 
where c.emailaddress in (
 	select distinct(aa.emailaddress)
 	from author_analyse aa)
 and c.author_id < 900000000;


-- usernames van onbekende gebruikers, die voorkomen bij bekende gebruikers
select count(distinct(c.username)), count(c.username) -- 3, 183
from commitinfo c 
where c.emailaddress in (
 	select distinct(aa.username)
 	from author_analyse aa)
 and c.author_id < 900000000;




-- combinatie username, emailadres in verschillende projecten. -- 35 keer bij 16 combinaties, mogelijk tellen wij hier 19 keer teveel, en missen wij programmeurs die bij verschillende projecten werken. 
select ab.username, ab.emailaddress, ab.project_id, ab.author_id 
from author_analyse ab 
where ab.concatenatie_ue in (
	select aa.concatenatie_ue
	from author_analyse aa
	group by aa.concatenatie_ue
    having count(aa.project_id) > 1)
order by ab.emailaddress ;

select distinct(ab.concatenatie_ue) as aantal_combinaties
from author_analyse ab 
where ab.concatenatie_ue in (
	select aa.concatenatie_ue
	from author_analyse aa
	group by aa.concatenatie_ue
    having count(aa.project_id) > 1);


-- alternatieve oplossing, niet kijken naar project wanneer wij een combinatie willen toekennen
   select count(c.author_id)
	from commitinfo c, author_analyse a 
	where c.username = a.username 
--	where   c.emailaddress = a.emailaddress 
	and   c.author_id < 900000000;
	
update author_analyse a 
set alternatief_id = (
	select count(c.author_id)
	from commitinfo c, author_analyse a 
	where c.username = a.username 
	and   c.emailaddress = a.emailaddress 
	and   c.author_id < 900000000
	
);
select count(*)
from author_analyse 
where alternatief_id is null;
