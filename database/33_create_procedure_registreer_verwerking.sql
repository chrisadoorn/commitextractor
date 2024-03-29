-- PROCEDURE: test.registreer_verwerking(bigint, character varying)

-- DROP PROCEDURE IF EXISTS test.registreer_verwerking(bigint, character varying);

CREATE OR REPLACE PROCEDURE registreer_verwerking(
	IN p_projectid bigint,
	IN p_resultaat character varying)
LANGUAGE 'plpgsql'
AS $BODY$


BEGIN

insert into verwerking_geschiedenis (project_id, project_naam, start_verwerking, einde_verwerking, processor, status, resultaat, processtap)
  select p_projectid, v.naam, v.start_verwerking, now(), v.processor, 'gereed', p_resultaat, v.processtap
  from verwerk_project v
  where id = p_projectid;

update verwerk_project
set einde_verwerking = now()
   ,status = 'gereed'
   ,resultaat = p_resultaat
   ,processor = null
where id = p_projectid;


END;
$BODY$;

GRANT EXECUTE ON PROCEDURE registreer_verwerking(bigint, character varying) TO appl;
