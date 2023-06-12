-- PROCEDURE: registreer_processor(character, bigint)

-- DROP PROCEDURE IF EXISTS registreer_processor(character, bigint);

CREATE OR REPLACE PROCEDURE registreer_processor(
	IN p_identifier character,
	INOUT p_new_id bigint)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN


insert into processor ("identifier")
values (p_identifier)
RETURNING "id" INTO p_new_id;

return;

END;
$BODY$;

GRANT EXECUTE ON PROCEDURE registreer_processor(character, bigint) TO appl;
