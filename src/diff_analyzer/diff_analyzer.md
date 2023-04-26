The diff analyzer module check all bestandswijziging for the existence of certein keywords in the difftext, the abbreviated change as notated by the git system. 

It is controlled by the existing list of processes in the verwerk_project table. 
The module overwrites existing analyses for the bestandswijziging in question.
The analysis is based on the script read_diff.py. 
If this script is changed the analysis should be repeated. 
