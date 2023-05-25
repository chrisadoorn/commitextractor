
set schema 'test';
-- PROCEDURE: verwerk_volgend_project(character, character varying, character varying, bigint, character varying, integer)
-- DROP PROCEDURE IF EXISTS verwerk_volgend_project(character, character varying, character varying, bigint, character varying, integer);

CREATE OR REPLACE PROCEDURE verwerk_volgend_project(
	IN p_identifier character,
	IN p_vorige_stap character varying,
	IN p_nieuwe_stap character varying,
	INOUT p_new_id bigint,
	INOUT p_projectnaam character varying,
	INOUT p_rowcount integer)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
	v_processor bigint;
BEGIN

set schema 'test';

-- controleer of de processor nog mag doorwerken
SELECT id INTO v_processor
FROM processor
where identifier = p_identifier
and status = 'actief';
if not found then
    select 0 into p_rowcount;
	return;
end if;

-- select id en naam van maximaal 1 record
select id, naam, 0 INTO p_new_id, p_projectnaam, p_rowcount
from verwerk_project
where processor is null
and processtap = p_vorige_stap
and resultaat = 'verwerkt'
and status != 'geblokt'
LIMIT 1 ;

if not found then
-- er is niets meer te verwerken.
    select 0 into p_rowcount;
	return;
end if;

-- update record op basis van eerder gevonden id.
update verwerk_project
set start_verwerking = now()
   ,einde_verwerking = null
   ,processor = p_identifier
   ,status = 'bezig'
   ,processtap = p_nieuwe_stap
where processor is null
and processtap = p_vorige_stap
and resultaat = 'verwerkt'
and status != 'geblokt'
and id =  p_new_id;

-- update de rowcount van default 0 naar aantal geupdate rijen.
-- als dit 0 is, dan is de update mislukt, en was een andere processor eerder.
if not found then
	select 0 into p_rowcount;
else
	select 1 into p_rowcount;
end if;



return;

END;
$BODY$;
ALTER PROCEDURE verwerk_volgend_project(character, character varying, character varying, bigint, character varying, integer)
    OWNER TO appl;
