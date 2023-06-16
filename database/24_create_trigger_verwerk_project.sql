-- FUNCTION: insert_verwerk_project()
CREATE OR REPLACE FUNCTION insert_verwerk_project()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
	begin

	    insert into verwerk_project(id
		                           ,naam
		                           ,locatie
		                           ,status
		                           ,resultaat
		                           ,processtap)
		values(new.id
		      ,new.naam
		      ,(select s.locatie from selectie s where s.id = new.idselectie)
		      ,'gereed'
		      ,'verwerkt'
		      ,'selectie'
		      );

		RETURN new;

	END;
$BODY$;



-- Trigger: project_insert_trigger
CREATE OR REPLACE TRIGGER project_insert_trigger
    AFTER INSERT
    ON project
    REFERENCING NEW TABLE AS new
    FOR EACH ROW
    EXECUTE FUNCTION insert_verwerk_project();