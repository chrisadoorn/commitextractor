SET schema 'prod';

alter table commitinfo add author_id Integer;
CREATE INDEX commitinfo_idauthor_idx ON commitinfo USING btree (author_id);