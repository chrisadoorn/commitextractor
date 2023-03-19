import os

from flask import Flask, render_template

from src.models.models import GhSearchSelection, CommitInformation, FileChanges

POSTGRESQL = 'postgresql'
CONFIGFILE = 'config.ini'
APP_DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/selected/")
def form_gh_search():
    ghs = GhSearchSelection.select().where(GhSearchSelection.selected_for_survey)
    return render_template('selected.html', latest_selection_list=ghs)


@app.route("/showgithub/<select_id>/detail/")
def form_commits_for_projects(select_id):
    selection = GhSearchSelection.select().where(GhSearchSelection.id == select_id)
    commits = CommitInformation.select().where(CommitInformation.id_project == select_id)
    return render_template('detail.html', commits=commits, selection=selection)


@app.route("/showgithub/<commit_id>/files/")
def files(commit_id):
    selections = FileChanges.select().where(FileChanges.id_commit == commit_id)
    return render_template('files.html', selections=selections)
