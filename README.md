# commitextractor
 extracts GitHub code changes

#### Aim of the program
This program uses pydriller (https://github.com/ishepard/pydriller) to extract code changes from projects within GitHub.
A list of projects is first stored in the database. The projects in this list are then downloaded by pydriller, which then loops through all its commits.
For each commit the files that are being changed are saved to database for further analysis by other functionality.

#### Requirements
See _installation.md_

## How to use
First a list of projects has to be loaded. Next the commitextractor can be started. 
Depending on the number and size of the projects, the program can run for days or even weeks.
To monitor the process, and to be able to intervene, see monitoring.md 

### loading projects.
The commitextractor processes a list of projects which are stored in the verwerk_project table.
To load those projects the following procedures are possible.

##### use selection loader module
When using GHsearch (https://seart-ghs.si.usi.ch/) it is possible to download a json file of the selection you made on the website.
Place this file in the data directory, and refer to this file in the ini file. (see var/ini.md)
You are now able to run the module selection loader, without further configuration.
When the module is finished, you will have your list of projects in the table verwerk_project.
Additionally, there is metadata about the projects and the selection stored in the tables project and selection.

##### manual insert  
At all times it is possible to manipulate the contents of the tables. 
When the projects are in a way selected which does not result in a supported format, you can make your own insert staements.
Take note of the dependencies within the database. (see database/database.md)

### running the commitextractor
The repo_extractor module downloads the projects and stores information about commits and file changes. 
It processes this one project at a time. In the ini file (see var/ini.md) you can configure the number of parallel processes.  
You have to add a list file extensions you are interested in. only files with one of those extensions will be filtered
After the module has finished the tables commitinfo and bestandswijziging are filled. 
If a project fails, and you want to retry, you have to take into account that commits and file changes that are already stored during the first attempt will stay there. 
You have to delete those before a second run. 

### Author identification
The author identification module is only compatible with GitHub project. It determines which author has written a file change by looking at the combination of username and email adress, as well as information through the GitHub api.
To run the module you have to have a GitHub token (https://github.com/settings/tokens) and store it in the ini file. 
After running the module each commit will have an author id attributed. If there are problems during processing, a new run will process only those commits for which the author is yet unknown.  

### Text search 

### Diff analyzer

### Parsers




