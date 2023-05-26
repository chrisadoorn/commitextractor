Deze map is voor experimenten Evert 


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
install depencies:
Als je venv gebruikt dat wordt alles daar geinstalleerd, anders globaal
```
pip install Flask
pip install peewee
pip install psycopg2-binary
pip install pydriller
```

Elixir embedded expressions #{}
"Embedded expression: #{3 + 0.14}"
Multiline strings:
"
This is
a multiline string
"
sigils. ~s()
iex(5)> ~s(This is also a string)
"This is also a string"

iex(6)> ~s("Do... or do not. There is no try." -Master Yoda)
"\"Do... or do not. There is no try.\" -Master Yoda"
heredocs syntax
iex(9)> """
Heredoc must end on its own line """
"""

iex(1)> 'ABC'
'ABC'
character list

iex(2)> [65, 66, 67]
'ABC'

iex(3)> 'Interpolation: #{3 + 0.14}'
'Interpolation: 3.14'
iex(4)> ~c(Character list sigil)
'Character list sigil'
iex(5)> ~C(Unescaped sigil #{3 + 0.14})
'Unescaped sigil \#{3 + 0.14}'
iex(6)> '''
Heredoc
'''
'Heredoc\n'
Character lists aren’t compatible with binary strings.