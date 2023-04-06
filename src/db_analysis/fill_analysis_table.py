import logging
from peewee import fn
from src.models.analysis_models import Analyse
from src.models.models import Project, CommitInfo, BestandsWijziging
from src.utils import configurator

global db_connectie

keywords = configurator.get_keywords()

def start_fill_analysis_table():
    file_changes = Analyse()

    for t in BestandsWijziging.select():
        # hoe via de foreign key makkelijk iets ophalen?
        file_changes.idproject =

        # hoe via de foreign key makkelijk iets ophalen?
        file_changes.idcommit =

        file_changes.idbestand = t.id

        # hoe via de foreign key makkelijk iets ophalen?
        file_changes.committer_name =

        # hoe via de foreign key makkelijk iets ophalen?
        file_changes.committer_emailaddress =

        # keywords vanuit analysis.ini en mee integreren in query of via een in-statement (cfr. commit_extractor.py)
        # select naam, difftext
        # from test.bestandswijziging as bestandswijziging,
        # 	 test.project as project,
        # 	 test.commitinfo as commits
        # where bestandswijziging.difftext ilike '%std::thread%'
        # 	  and commits.idproject = project.id
        # 	  and commits.idcommit = bestandswijziging.idcommit

        file_changes.keyword =

        # LoC tellen via ModifiedFile nloc: Lines Of Code (LOC) of the file
        file_changes.loc =


