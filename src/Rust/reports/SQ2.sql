--SQ.2 What is the correlation between multi-core programming primitives and the percentage of programmers using them?

--SQL statements voor het beantwoorden van SQ2
--primitives and number of uses
select zoekterm, count(idbestandswijziging) as freq
from test.bestandswijziging_zoekterm
where falsepositive = 'False'
group by zoekterm
order by freq desc

--per zoekterm # aantal verschillende programmeurs en totale frequentie
select  bz.zoekterm, count(distinct(author_id)), count(bz.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.idbestandswijziging = b.id
     and bz.falsepositive = 'False'
group by bz.zoekterm

--per auteur verschillende zoektermen count
 SET SCHEMA 'test';
CREATE OR REPLACE VIEW auteur_verschillendeZoektermen
AS SELECT
     author_id, count(distinct(bz.zoekterm)) as freq1
    from test.bestandswijziging_zoekterm bz,
         test.bestandswijziging b,
         test.commitinfo ci
    where b.idcommit = ci.id
          and bz.idbestandswijziging = b.id
         and bz.falsepositive = 'False'
    group by author_id


--per bib # aantal verschillende programmeurs en totale frequentie

--async/await
select count(distinct(author_id)), count(bz.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.idbestandswijziging = b.id
     and bz.falsepositive = 'False'
     and bz.zoekterm in ('.await')

--threads
select count(distinct(author_id)), count(bz.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.idbestandswijziging = b.id
     and bz.falsepositive = 'False'
     and bz.zoekterm in ('thread::Builder::new','thread::spawn')

--sync
select count(distinct(author_id)), count(bz.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.idbestandswijziging = b.id
     and bz.falsepositive = 'False'
     and bz.zoekterm in ('.recv()','.send(%)','Arc::new','Barrier::new','Condvar::new',
		'Mutex::new','Once::new','OnceLock::new','channel()','channel::','sync_channel(%)',
		'sync_channel::')

--concurrency crates
select count(distinct(author_id)), count(bz.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.idbestandswijziging = b.id
     and bz.falsepositive = 'False'
     and bz.zoekterm not in ('.recv()','.send(%)','Arc::new','Barrier::new','Condvar::new',
		'Mutex::new','Once::new','OnceLock::new','channel()','channel::','sync_channel(%)',
		'sync_channel::','thread::Builder::new','thread::spawn','.await')

