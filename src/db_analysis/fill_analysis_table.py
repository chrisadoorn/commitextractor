import logging
from peewee import fn
from src.models.analysis_models import Analyse
from src.models.models import Project, CommitInfo, BestandsWijziging
from src.utils import configurator

global db_connectie

keywords = configurator.get_keywords()

def start_fill_analysis_table():
    file_changes = Analyse()

    split_up = os.path.splitext(file.filename)
    # bestand is apart genoemd
    if file.new_path in files:

    for t in BestandsWijziging.select().where(BestandsWijziging.difftext.contains('tennis')):

        split_up = os.path.splitext(file.filename)
        # bestand is apart genoemd

            query = Facility.select()

            # hoe via de foreign key makkelijk iets ophalen?
            file_changes.idproject = t.Project.id

            # hoe via de foreign key makkelijk iets ophalen?
            file_changes.idcommit = t.CommitInfo.id

            file_changes.idbestand = t.BestandsWijziging.id

            # hoe via de foreign key makkelijk iets ophalen?
            file_changes.committer_name = t.CommitInfo.username

            # hoe via de foreign key makkelijk iets ophalen?
            file_changes.committer_emailaddress = t.CommitInfo.emailaddress

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


