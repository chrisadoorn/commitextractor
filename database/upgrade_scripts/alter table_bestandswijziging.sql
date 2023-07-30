-- nieuwe kolommen
alter table bestandswijziging
add uitgesloten boolean default false,
add uitsluitreden character varying NULL;

-- all done
