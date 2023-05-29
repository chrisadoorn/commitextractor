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
```

Elixir uses the BEAM virtual created for Erlang. (from Elixir in Action)

Why Erlang/Elixir?
Highly available systems, that run forever, that always respond to client requests.

How to accomplish this:
 - Fault-tolerance — Minimize, isolate, and recover from the effects of runtime errors.
 - Scalability — Handle a load increase by adding more hardware resources without
     changing or redeploying the code.
 - Distribution — Run your system on multiple machines so that others can take over
       if one machine crashes.

If you address these challenges, your systems can constantly provide service with minimal downtime and failures

Parallelism and concurrency are a key parts of the solution.

BEAM runs in one OS process and creates (by default) for each core a OS thread, each OS thread has a scheduler.
Multiple cores are needed for parallelism.
The schedulers use preemption, based on a timeslot, to ensure that all processes get a chance to run.
BEAM processes are lightweight, a few kb, don't share memory, completely isolated.

Found mc primitives:
```
Process.sleep()

spawn/1
spawn(fn ->
    expression_1
        ...
    expression_n
end)

spawn(fn -> IO.puts(run_query.("query 1")) end)
```

A process can send a message to another process, the message is put in the mailbox of the receiving process.
These are asynchronous, the sender doesn't wait for a response.
This mailbox is a queue, the messages are processed in the order they arrive.
Limited to memory.

It will process messages by pattern matching.


```
send(pid, {:an, :arbitrary, :term})

receive do
  pattern_1 -> do_something
  pattern_2 -> do_something_else
end

```

A process may keep itself running by using a recursive loop, when using tail recursion it won't consume additional memory.

```
defp loop do
  receive do
   ...
  end
  loop()
end
```

