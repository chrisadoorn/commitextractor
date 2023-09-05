select  number_of_languages, id, naam, languages  
from project p 
where number_of_languages = (select max(number_of_languages) from project i where i.idselectie = 1)
and p.idselectie = 1;

select  number_of_languages, id, naam, languages  
from project p 
where languages like '%Elixir%'
or  languages like '%Rust%'

-- 182 op 94.483 like '%Rust%' 
-- like 'lixer'
select count(*) from project;

select  count(*)                 --26.854 op 94.483
from project p 
where number_of_languages > 1
and p.idselectie = 1;           --   311 op 1.090