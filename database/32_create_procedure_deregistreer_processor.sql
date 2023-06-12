-- PROCEDURE: deregistreer_processor(character)

-- DROP PROCEDURE IF EXISTS deregistreer_processor(character);

CREATE OR REPLACE PROCEDURE deregistreer_processor(
	IN p_identifier character)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN


update processor
set status = 'gestopt'
   ,einde_processing = now()
where identifier = p_identifier;
return;

END;
$BODY$;

GRANT EXECUTE ON PROCEDURE deregistreer_processor(character) TO appl;
