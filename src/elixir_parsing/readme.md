# Elixir parsing

This part contains a program written in Elixir and a module written in Python.

## Elixir program

To run the Elixir program, you need to have Elixir installed on your computer.
You can find more information about this [here](https://elixir-lang.org/install.html).

The Elixir has 2 functions: create ASTs and tokenize the source code of a project.
To tokenize set this value in the start function of the application.exs file:
```
AstCreator.System
```  
To create ASTs set this value in the main function of the application.exs file:
```
AstCreator.System2
```
Make sure the abstract_syntax_trees db table exists in the database.
The create table query can be found in the elixir_create_ast_table.sql file.

Run the Elixir program using the following commands:
```
iex -S mix
```

## Python module
This module reads the tokenized source code from the database and analyses it.
It checks if the bestandswijziging_zoekterm_regelnummer records are valid, that 
means it is present in a certain format in the tokenized code.


# Run the module

To module will read the content of verwerk_project table in the database.
It will process all projects from this table where the value of processtap is 'extractie'.
You may have to set this value manually in the database if you want to run this module again.

```sql
--update query:
update verwerk_project set processtap = ' ', resultaat = 'verwerkt', start_verwerking = null, einde_verwerking = null;
```

To run start the main method of the main module.
The code wil run in parallel.
