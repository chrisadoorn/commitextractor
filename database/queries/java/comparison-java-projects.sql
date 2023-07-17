-- selecteer een aantal metrieken
SELECT id, naam,
main_language,
cast(languages::json->>'Java' as int) as java_bytes,
cast(languages::json->>'Java' as int) / 1024  as java_kb,
project_size as project_kb,
contributors,
number_of_languages,
languages
	FROM project
	order by number_of_languages desc;


-- tellingen
select count(*) from project; 						-- alle GHSearch
select count(*) from project where idselectie = 1;  -- geselecteerd 1099
select count(*) from project where idselectie = 1   -- alles verwerkt 1082
and id in ( select id from verwerk_project vp where resultaat = 'verwerkt'); 
select count(*) from project where idselectie = 1   -- alles mislukt 17
and id in ( select id from verwerk_project vp where resultaat = 'mislukt'); 

-- gemiddeldes
select -- alle projecten
	 to_char(avg(contributors), '999,999.9') as avg_contributors  	--    9.4
	,to_char(avg(project_size), '999,999.9') as avg_project_kb  	--	25,836.4
	,to_char(avg(cast(languages::json->>'Java' as int)/ 1024), '999,999.9') as avg_java_kb  		-- 2,295.0
	,to_char((avg(cast(languages::json->>'Java' as int)/ 1024) /avg(project_size))*100, '999.9')  as perc_java_vs_all_code	
	,to_char(avg(number_of_languages), '999,999.9') as avg_languages 		-- 1.5
	FROM project;

select -- sample
	 to_char(avg(contributors), '999,999.9') as avg_contributors  	--    9.4
	,to_char(avg(project_size), '999,999.9') as avg_project_kb  	--	25,836.4
	,to_char(avg(cast(languages::json->>'Java' as int)/ 1024), '999,999.9') as avg_java_kb  		-- 2,295.0
	,to_char((avg(cast(languages::json->>'Java' as int)/ 1024) /avg(project_size))*100, '999.9')  as perc_java_vs_all_code	
	,to_char(avg(number_of_languages), '999,999.9') as avg_languages 		-- 1.5
	FROM project
 where idselectie = 1;

select -- verwerkt
	 to_char(avg(contributors), '999,999.9') as avg_contributors  	--    9.4
	,to_char(avg(project_size), '999,999.9') as avg_project_kb  	--	25,836.4
	,to_char(avg(cast(languages::json->>'Java' as int)/ 1024), '999,999.9') as avg_java_kb  		-- 2,295.0
	,to_char((avg(cast(languages::json->>'Java' as int)/ 1024) /avg(project_size))*100, '999.9')  as perc_java_vs_all_code	
	,to_char(avg(number_of_languages), '999,999.9') as avg_languages 		-- 1.5
	FROM project
 where idselectie = 1
and id in ( select id from verwerk_project vp where resultaat = 'verwerkt');

select -- mislukt
	 to_char(avg(contributors), '999,999.9') as avg_contributors  	--    9.4
	,to_char(avg(project_size), '999,999.9') as avg_project_kb  	--	25,836.4
	,to_char(avg(cast(languages::json->>'Java' as int)/ 1024), '999,999.9') as avg_java_kb  		-- 2,295.0
	,to_char((avg(cast(languages::json->>'Java' as int)/ 1024) /avg(project_size))*100, '999.9')  as perc_java_vs_all_code	
	,to_char(avg(number_of_languages), '999,999.9') as avg_languages 		-- 1.5
	FROM project
 where idselectie = 1
and id in ( select id from verwerk_project vp where resultaat = 'mislukt');


-- Hieronder: hoe telt het als ik de gevallen waar er geen git clone was neem
select -- verwerkt
	 to_char(avg(contributors), '999,999.9') as avg_contributors  	--    9.4
	,to_char(avg(project_size), '999,999.9') as avg_project_kb  	--	25,836.4
	,to_char(avg(cast(languages::json->>'Java' as int)/ 1024), '999,999.9') as avg_java_kb  		-- 2,295.0
	,to_char((avg(cast(languages::json->>'Java' as int)/ 1024) /avg(project_size))*100, '999.9')  as perc_java_vs_all_code	
	,to_char(avg(number_of_languages), '999,999.9') as avg_languages 		-- 1.5
	FROM project
 where idselectie = 1
and id in ( select id from verwerk_project vp where resultaat = 'verwerkt')
or id in (10493,68801,79551, 92623)

select -- mislukt
	 to_char(avg(contributors), '999,999.9') as avg_contributors  	--    9.4
	,to_char(avg(project_size), '999,999.9') as avg_project_kb  	--	25,836.4
	,to_char(avg(cast(languages::json->>'Java' as int)/ 1024), '999,999.9') as avg_java_kb  		-- 2,295.0
	,to_char((avg(cast(languages::json->>'Java' as int)/ 1024) /avg(project_size))*100, '999.9')  as perc_java_vs_all_code	
	,to_char(avg(number_of_languages), '999,999.9') as avg_languages 		-- 1.5
	FROM project
 where idselectie = 1
and id in ( select id from verwerk_project vp where resultaat = 'mislukt')
and id  in (10493,68801,79551, 92623)


select id from project p where 
naam in ('n3o-d4rk3r/competitive-programming-reference-bangla','apache/maven-javadoc-plugin','mirror/jdownloader','castello/spring_basic');

