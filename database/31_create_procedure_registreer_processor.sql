-- PROCEDURE: test.registreer_processor(character, bigint)

-- DROP PROCEDURE IF EXISTS test.registreer_processor(character, bigint);

CREATE OR REPLACE PROCEDURE test.registreer_processor(
	IN p_identifier character,
	INOUT p_new_id bigint)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN

set schema 'test';
insert into processor ("identifier")
values (p_identifier)
RETURNING "id" INTO p_new_id;

return;

END;
$BODY$;
ALTER PROCEDURE test.registreer_processor(character, bigint)
    OWNER TO appl;
