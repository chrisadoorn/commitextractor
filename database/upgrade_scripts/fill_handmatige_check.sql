INSERT INTO handmatige_check (projectnaam,
    project_id,
    bwz_id,
    zoekterm,
    falsepositive,
    regelnummers,
    bestandswijziging_id,
    commit_datum,
    commit_sha,
    commit_remark)
select  p.naam, p.id,  bz.id, bz.zoekterm, bz.falsepositive, bz.regelnummers, bz.idbestandswijziging, c.commitdatumtijd, c.hashvalue, c.remark
from prod.bestandswijziging_zoekterm bz, prod.bestandswijziging b, prod.commitinfo c, prod.project p
where  bz.idbestandswijziging = b.id
and b.idcommit = c.id and c.idproject = p.id
order by p.id, c.commitdatumtijd, c.hashvalue ;

