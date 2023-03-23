Query voor join project, commits en filechanges

```postgresql
select g.name, ci.*, f.* from ghsearchselection g 
    join commitinformation ci on g.id = ci.id_project
    join filechanges f on ci.id_project = f.id_project 
                         where f.id_project = :project_id
    order by commit_date_time;
```
Zoek naar spawn 
```postgresql
select g.name, ci.*, f.* from ghsearchselection g  
    join commitinformation ci on g.id = ci.id_project
    join filechanges f on ci.id_project = f.id_project 
                         where f.id_project = :project_id and extension ='.ex' and f.diff_text like '%spawn%'
    order by commit_date_time;
```

Gebruik van virtualenv
```
sudo apt-get install python3-pip
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```
Probeer alles in venv te installeren:

Zorg je in de virtual environment zit:
```
source venv/bin/activate
```

dependencies:
   - peewee
   - psycopg2-binary
   - pydriller

start webapp:
```
PYTHONPATH=~/IdeaProjects/commitextractor/ python main.py
```
linux command:
```
lsof -i :5000
pidof python
kill -9 pid
```