-- vervang irritante enkel quote in de naam van een programmeertaal
update project
set languages = replace(languages, 'Cap''n', 'Capn')
where languages like '%Cap%';

-- vervang enkele quotes binnen de json string met languages
update project
set languages = replace(languages,'''', '"' )
;
