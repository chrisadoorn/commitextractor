set schema 'v11';


CREATE TEMPORARY TABLE IF NOT EXISTS result_table
(
    cnt varchar,
    c integer,
    perc numeric,
    conf numeric
);


truncate table result_table;


DO $$DECLARE r record;
BEGIN
    for r in select count(*) as c from v11.authors_languages
        loop
            insert into result_table
            select
                ls.l_name,
                count(distinct ls.id) as count,
                round(count(distinct ls.id)/(r.c/100.0),1),
                round(1.96 * sqrt( count(distinct ls.id)/(r.c/100.0)  * (100 - count(distinct ls.id)/(r.c/100.0)) / r.c),1)
            from
                (select id , unnest(string_to_array(languages, ';')) as l_name from v11.authors_languages al

                ) as ls
            group by ls.l_name;
        end loop;

END$$;

select * from result_table order by c desc;

