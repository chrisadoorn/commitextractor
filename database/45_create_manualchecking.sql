set schema 'test';


DROP TABLE IF EXISTS manualchecking;

CREATE TABLE manualchecking (
	id serial4 NOT NULL,
	idproject int4 NOT NULL,
	"comment" text NULL,
	type_of_project varchar(255) NULL,
	"exclude" bool NULL,
	exclude_reason varchar(255) NULL,
	CONSTRAINT manualchecking_pkey PRIMARY KEY (id)
);
CREATE INDEX manualchecking_idproject ON manualchecking USING btree (idproject);

-- Permissions

ALTER TABLE manualchecking OWNER TO postgres;
GRANT ALL ON TABLE manualchecking TO postgres;


-- dev.manualchecking foreign keys

ALTER TABLE manualchecking ADD CONSTRAINT manualchecking_idproject_fkey FOREIGN KEY (idproject) REFERENCES project(id) ON DELETE CASCADE;