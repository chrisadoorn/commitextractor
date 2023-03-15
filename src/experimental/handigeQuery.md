Query voor join project, commits en filechanges

```
select g.name, ci.*, f.* from ghsearchselection g join commitinformation ci on g.id = ci.id_project
join filechanges f on ci.id_project = f.id_project where f.id_project = :project_id
order by commit_date_time;
```