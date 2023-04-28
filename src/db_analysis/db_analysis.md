The db analysis analyzer module checks all bestandswijziging for the existence of certain keywords in the difftext, the abbreviated change as notated by the git system. 

Fill_zoekterm_table.py takes the keywords from var/analysis.ini & uploads them in table zoekterm

Fill_analysis_table.py takes these keywords 1 by 1 and checks if they appear in column difftext from table bestandswijziging. 
If so, the results (id bestandswijziging & keyword) are uploaded in table bestandswijziging zoekterm.

