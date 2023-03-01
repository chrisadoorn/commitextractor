# commitextractor
 extracts GitHub code changes

#### Aim of the program
This program uses pydriller (https://github.com/ishepard/pydriller) to extract code changes from projects within GitHub.
A list of projects is first stored in the database. The projects in this list are then downloaded by pydriller, which then loops through all its commits.
For each commit the files that are being changed are saved to database for further analysis by other functionality.

#### Requirements
This program needs a python runtime ( 3.11 or higher).
This program needs a postgresql database.

#### How to use


##### Altering the number of running processes.


### The modules

##### commitextractor

##### configurator

##### db_postgresql

##### hashing

##### load_ghsearch
This module makes it possible to fill the database with a list of projects. It can only 

##### main

##### parallelizer
The parallelizer is a small module used to start multiple processes parallel to each other.
Each process registers itself in the database, and deregisters itself on closing. 

##### sanitychecker
The sanitychecker is called when the program is started to confirm that a basisc configuration is working.
It checks database connectivity, as well as the availabilty and proper configuration of paarameters.



