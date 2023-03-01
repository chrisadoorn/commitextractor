set schema 'test';

-- PROCEDURE: verwerk_volgend_project(char(36), bigint, varchar, int)

-- DROP PROCEDURE IF EXISTS verwerk_volgend_project( char(36), bigint, varchar, int);

-- p_identifier: de processor die om een nieuw project vraagt
-- p_new_id: het id van het gevonden project als output
-- p_projectnaam: de naam van het gevonden project als output
-- p_rowcount: 1 las de actie succesvol was, 0 anders,  als output

CREATE OR REPLACE PROCEDURE verwerk_volgend_project(
	IN p_identifier char(36),
	INOUT p_new_id bigint,
	INOUT p_projectnaam varchar,
    INOUT p_rowcount int)
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
    p_rowcount = 0;
	return;
end if;


-- select id en naam van maximaal 1 record
select id, naam, 0 INTO p_new_id, p_projectnaam, p_rowcount
from verwerk_project
where processor is null
and status = 'nieuw'
LIMIT 1 ;

if not found then
-- er is niets meer te verwerken.
    p_rowcount = 0;
	return;
end if;

-- update record op basis van eerder gevonden id.
update verwerk_project
set start_extractie = now()
   ,processor = p_identifier
   ,status = 'bezig'
where processor is null
and status = 'nieuw'
and id =  p_new_id;

-- update de rowcount van default 0 naar aantal geupdate rijen.
-- als dit 0 is, dan is de update mislukt, en was een andere processor eerder.
get diagnostics p_rowcount = row_count;

return;

END;
$BODY$;
ALTER PROCEDURE verwerk_volgend_project( char(36), bigint, varchar, int)
    OWNER TO appl;
