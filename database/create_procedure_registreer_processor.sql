set schema 'test';

-- PROCEDURE: registreer_processor( char(36), bigint)

--DROP PROCEDURE IF EXISTS registreer_processor( char(36), bigint);

CREATE OR REPLACE PROCEDURE registreer_processor(
	IN p_identifier char(36),
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
ALTER PROCEDURE registreer_processor( char(36), bigint)
    OWNER TO appl;
