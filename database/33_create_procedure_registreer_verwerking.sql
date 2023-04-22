set schema 'test';
-- PROCEDURE: test.registreer_verwerking(bigint, character varying)

-- DROP PROCEDURE IF EXISTS test.registreer_verwerking(bigint, character varying);

CREATE OR REPLACE PROCEDURE registreer_verwerking(
	IN p_projectid bigint,
	IN p_resultaat character varying)
LANGUAGE 'plpgsql'
AS $BODY$


BEGIN

update verwerk_project
set einde_verwerking = now()
   ,status = 'gereed'
   ,resultaat = p_resultaat
   ,processor = null
where id = p_projectid;

END;
$BODY$;
ALTER PROCEDURE registreer_verwerking(bigint, character varying)
    OWNER TO appl;

GRANT EXECUTE ON PROCEDURE registreer_verwerking(bigint, character varying) TO PUBLIC;

GRANT EXECUTE ON PROCEDURE registreer_verwerking(bigint, character varying) TO appl;

