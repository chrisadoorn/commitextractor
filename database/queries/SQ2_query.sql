--SQ.2 What is the correlation between multi-core programming primitives and the
-- percentage of programmers using them?

-- Query:
select b.author_id, count(distinct(d.zoekterm)) as verschillende_zoektermen
	from project a,
     commitinfo b,
     bestandswijziging c,
     bestandswijziging_zoekterm d
	where a.id = b.idproject
        and b.id = c.idcommit
        and c.id = d.idbestandswijziging
group by b.author_id
order by verschillende_zoektermen desc;

