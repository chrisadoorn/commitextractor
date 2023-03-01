-- PROCEDURE: test.registreer_verwerking(bigint, character varying)

-- DROP PROCEDURE IF EXISTS test.registreer_verwerking(bigint, character varying);

CREATE OR REPLACE PROCEDURE test.registreer_verwerking(
	IN p_projectid bigint,
	IN p_resultaat character varying)
LANGUAGE 'plpgsql'
AS $BODY$

BEGIN

set schema 'test';

update verwerk_project
set einde_extractie = now()
   ,status = 'gereed'
   ,resultaat = p_resultaat
where id = p_projectid;

END;
$BODY$;
ALTER PROCEDURE test.registreer_verwerking(bigint, character varying)
    OWNER TO appl;
