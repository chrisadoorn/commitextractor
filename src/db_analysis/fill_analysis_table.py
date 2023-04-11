import logging
from peewee import fn
from src.models.analysis_models import Analyse
from src.models.models import Project, CommitInfo, BestandsWijziging
from src.utils import configurator

global db_connectie



def start_fill_analysis_table():
    file_changes = Analyse()
    keywords = configurator.get_keywords()
    #print(BestandsWijziging.select().where(BestandsWijziging.difftext.contains("extensions")))


    print(BestandsWijziging.select().where(BestandsWijziging.difftext.contains("threads")).count())

    #for x in range(len(keywords)):
        #for t in BestandsWijziging.select().where(BestandsWijziging.difftext.contains(keywords[x])):

        #for t in BestandsWijziging.select():
                #print(t.id)
                #file_changes.idproject = t.Project.id
                #print(t.Project.id)
                #file_changes.idcommit = t.CommitInfo.id
                #file_changes.idbestand = t.BestandsWijziging.id
                #file_changes.committer_name = t.CommitInfo.username
                #file_changes.committer_emailaddress = t.CommitInfo.emailaddress
                #file_changes.keyword = keywords[x]
                # LoC tellen via ModifiedFile nloc: Lines Of Code (LOC) of the file
                #file_changes.loc = 0


start_fill_analysis_table()

