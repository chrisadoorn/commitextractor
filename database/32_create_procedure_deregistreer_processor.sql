-- PROCEDURE: test.deregistreer_processor(character)

-- DROP PROCEDURE IF EXISTS test.deregistreer_processor(character);

CREATE OR REPLACE PROCEDURE test.deregistreer_processor(
	IN p_identifier character)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN

set schema 'test';
update processor
set status = 'gestopt'
   ,einde_processing = now()
where identifier = p_identifier;
return;

END;
$BODY$;
ALTER PROCEDURE test.deregistreer_processor(character)
    OWNER TO appl;
