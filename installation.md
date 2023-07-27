# installation

### Requirements
This program needs: 
* python runtime (3.11 or higher).
* a postgresql database server, version 15 or higher.
* git to be in the Path
* a working internet connection.
* Java runtime (Java 11 or higher)

#### installing the application
* clone the project from GitHub: https://github.com/chrisadoorn/commitextractor 
* create a python virtual environment to work from
  ```shell
  cd commitextractor # root directory of project
  python3.11 -m venv venv
  source venv/bin/activate
  ```
* install dependencies
 ```shell
  pip install -r requirements.txt
  ```
#### creating the database structure
* On your postgresql server create a database. In the example, the name of the databse is _multicore_
```sqlite-psql
  CREATE DATABASE multicore
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
  ```
 * Create a user 'appl' with a password  
```sqlite-psql
  CREATE ROLE appl WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'xxxxxx';
  ```
* Generate the database schema
  * run the python script database/py_scripts/create_complete_schema.py. This will create a script that creates alle necessary within the database.
  * The script will create schema _prod_ as default. You can change this name in the script.
* Run the generated script when connected to the database with the same account you used to create the database.
  * The script can be found at database/temp/full_script.prod.sql. If you have changed the schema name, filename will be likewise changed. 

#### configuring the applicaton
* create the file var/commitextractor.ini. You can use var/commitextractor.example.ini as template
* Alter the connection parameters to the database, so they refer to the database and user you created earlier. These are under section [postgresql]. 
* Create a GitHub personal access API token. Follow instructions from https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
* Enter this token instead of _here_should_be_your_personal_github_access_token_
* Create the file var/commitextractor.seed. This file must contain a randomly chosen string. (We used a UUID as content).
* All other configuration items can work with the provided configuration. However, you may be interested to change the amount of logging, bu altering the loglevel. Or you may want to influence the number of parallel processes, by altering the _run_parallel_ parameter. 

#### testing the setup
Run the module _repo_extractor_ before any projects are selected. At the start of the module checks will be performed to connect to the database, to connect to the GitHub API and to see if a seed file is present. 
The results of these checks can be found in the logfile. 

#### installing parser support.
The ANTLR4 needs java support, JDK11 or higher. Download the jar file _antlr-4.13.0-complete.jar_ from https://www.antlr.org/download.html. 
Add the jar file to the environment variable _CLASSPATH_.  



   
