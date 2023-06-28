
CREATE OR REPLACE VIEW compare_analysis
AS SELECT  bz.zoekterm
, bz.falsepositive
,jpr.is_in_namespace
,jpr.is_gebruik_gewijzigd
,jpr.is_nieuw
,jpr.is_verwijderd
,jpr.bevat_unknown
,jpr.usage_list_achteraf
,jpr.usage_list_vooraf
, bz.regelnummers
, bz.aantalgevonden
, b.difftext
, b.tekstvooraf
,b.tekstachteraf
,b.id AS bestandswijzing_id
,bz.id AS bwz_id
from bestandswijziging_zoekterm bz
    ,java_parse_result jpr
    ,bestandswijziging b
where bz.id = jpr.id
and   bz.idbestandswijziging = b.id;

-- Permissions
GRANT SELECT ON TABLE compare_analysis TO appl;
