set schema 'test';

-- PROCEDURE: deregistreer_processor( char(36), bigint)

--DROP PROCEDURE IF EXISTS deregistreer_processor( char(36));

CREATE OR REPLACE PROCEDURE deregistreer_processor(
	IN p_identifier char(36))
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN

set schema 'test';
update processor
set status = 'gestopt'
   ,einde_processing = now();
where identifier = p_identifier
return;

END;
$BODY$;
ALTER PROCEDURE deregistreer_processor( char(36))
    OWNER TO appl;
