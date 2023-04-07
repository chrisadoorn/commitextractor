-- vervang irritante enkel quote in de naam van een programmeertaal
update prod.project
set languages = replace(languages, 'Cap''n', 'Capn')
where languages like '%Cap%';

-- vervang enkele quotes voor namen 
update project
set languages = replace(languages,'''', '"' )
;

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
