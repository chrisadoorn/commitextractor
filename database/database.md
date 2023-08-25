# Database description


![](../png/datamodel_20220325.png)

Our database has two functional and one technical part.

* tables containing the information on projects.
* tables containing the configuration and results of our analysis
* tables to control and monitor the process.

### tables containing the information on projects
We store information about the following entities:

#### Selectie
In the selectie table we store data about the selection we make, at which date and with which criteria.
This table stores the metadata for the reason why projects are selected.  

#### Project
The project table contains information about projects which are registered on GitHub. This data is valid at the moment of selection. If there is a gap between the moment of selection and the processing of the project, there might be a discrepancy. 
For instance, in the metadata the number of forks is noted. However, somebody might have made a new fork in the meantime. 
Each project references a selection, which indicates why the project is selected.

#### Commitinfo
The commitinfo table contains the metadata about git commits. 
When, by whom, comments, are all stored. 
Commitinfo relates to project.

#### Bestandswijziging
The bestandswijziging table contains information about filechanges. It contains the name of the file, the diff, the text after the change.
Bestandswijziging relates to commitinfo. 

### tables containing the analysis

#### Zoekterm
The table zoekterm contains the keywords that you are looking for.
The content depends on the language under study.
Each keyword is associated with the extension of the file you are looking in. 

#### Bestandswijziging_zoekterm
This table shows which keywords are found in which file. Records are inserted by the text search module.
In the next analysis steps the _falsepositive_ flag can be updated, as well as an reason filled in _afkeurreden_.
Bestandswijziging_zoekterm relates both to Bestandswijziging and Zoekterm.

#### Bestandswijziging_zoekterm_regelnummer
This table stores the line numbers where the keyword has been found.
Bestandswijziging_zoekterm_regelnummer relates to Bestandswijziging_zoekterm.

### tables to control and monitor the process
This is the technical part of the database.

To keep the data about the projects we process separate from the data about the proccing itself some extra tables have been added.
To be able to do parallel processing we have to administrate which processes are running,
and to be able to assign the correct work for those processes. 
Processes register and deregister themselves (by calling procedures), this information in the 'processor' table.
For each process, the state is kept the 'verwerk_project' table. 
This table is filled by a trigger when inserting a project. 
The content is modified by calling procedures. 
The procedures garantee that each project is only processed once, and that each project gets processed. 
Each project passes through several stages, the name of which is stored in column 'processtap'.
The status of the processing is indicated by filling the start time ( start_verwerking) and the id of the processor doing the work.
Also, the status is set to 'bezig'.
When a processor hasd finished processing a projects, the stop time is set ( einde_verwerking), the status is set to done ('verwerkt') and the result is indicated in 'resultaat'.
The result can be 'verwerkt' for succesfull processing or to 'mislukt' in case a failure has happened.
Only projects which are succesfully processed in the previous step are eligible for further processing.

The next table shows the processes in the sequence in which they are performed.

| name of proces step  | process                                          | performed by                      | step is registered? |
|----------------------|--------------------------------------------------|-----------------------------------|---------------------|
| selectie             | storing the list of project to be processed      | selection_loader/load_ghsearch.py | yes                 |
| extractie            | downloading the project and storing file changes | repo_extractor/main.py            | yes                 |
| identificatie        | determining the author of a filechange           | author_identifier/main.py         | yes                 |
| zoekterm_vinden      | determining which file changes contain keywords  | text_search/main.py               | yes                 |
| zoekterm_controleren | checking for false positives                     | diff_analyzer/main.py             | yes                 |
 