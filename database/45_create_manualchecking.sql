CREATE TABLE manualchecking (
	id BIGSERIAL PRIMARY KEY,
	idproject int4 NOT NULL,
	"comment" text NULL,
	type_of_project varchar(255) NULL,
	"exclude" bool NULL,
	exclude_reason varchar(255) NULL,
	CONSTRAINT manualchecking_idproject_fkey FOREIGN KEY (idproject)
	    REFERENCES project(id) ON DELETE CASCADE
);
CREATE INDEX manualchecking_idproject ON manualchecking USING btree (idproject);

-- Permissions
GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE manualchecking TO appl;
GRANT USAGE ON SEQUENCE manualchecking_id_seq TO appl;
