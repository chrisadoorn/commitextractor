SET schema 'test';

CREATE INDEX commitinfo_idproject_idx ON commitinfo USING btree (idproject);
CREATE INDEX bestandswijziging_idcommit_idx ON bestandswijziging USING btree (idcommit);
