# commitextractor
 extracts GitHub code changes

#### Aim of the program
This program uses pydriller (https://github.com/ishepard/pydriller) to extract code changes from projects within GitHub.
A list of projects is first stored in the database. The projects in this list are then downloaded by pydriller, which then loops through all its commits.
For each commit the files that are being changed are saved to database for further analysis by other functionality.

#### Requirements
This program needs: 
* python runtime (3.11 or higher).
* a connection to a postgresql database.
* git to be in the Path
* a working internet connection.

## How to use
First a list of projects has to be loaded. Next the commitextractor can be started. 
Depending on the number and size of the projects, the program can run for days or even weeks.
To monitor the process, and to be able to intervene, see monitoring.md 


### loading projects.
The commitextractor processes a list of projects which are stored in the verwerk_project table.
To load those projects the following procedures are possible.

##### use load_ghsearch.py
When using GHsearch (https://seart-ghs.si.usi.ch/) it is possible to download a json file of the selection you made on the website.
Place this file in the data directory, and refer to this file in the ini file. (see var/ini.md)
You are now able to run the module load_ghsearch.py, without further configuration.
When the program is finished, you will have your list of projects in the table verwerk_project.
Additionally, there is metadata about the projects and the selection stored in the tables project and selection.

##### manual insert  
At all times it is possible to manipulate the contents of the tables. 
When the projects are in a way selected which does not result in a supported format, you can make your own insert staements.
Take note of the dependencies within the database. (see database/database.md)

### running the commitextractor


##### Altering the number of running processes.
The parallelizer is used to run a configurable number of processes. 


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



