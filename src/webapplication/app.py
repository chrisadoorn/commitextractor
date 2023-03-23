import os

from flask import Flask, render_template

from src.models.models import GhSearchSelection, CommitInformation, FileChanges

POSTGRESQL = 'postgresql'
CONFIGFILE = 'config.ini'
APP_DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def form_gh_search():
    ghs = GhSearchSelection.select().where(GhSearchSelection.selected_for_survey)
    return render_template("selected.html", latest_selection_list=ghs)


commits_selection_in_memory: list = []


@app.route("/showgithub/<select_id>/detail/")
def form_commits_for_projects(select_id):
    selection_in_memory: GhSearchSelection = GhSearchSelection.select().where(GhSearchSelection.id == select_id)
    commits = CommitInformation.select().where(CommitInformation.id_project == select_id)
    for commit in commits:
        commit.selections_with_mc = get_files(commit.id)
    global commits_selection_in_memory
    commits_selection_in_memory = commits
    return render_template("detail.html",
                           commits=commits[0:10],
                           selection=selection_in_memory[0],
                           from_int=10,
                           to_int=20,
                           back_from_int=-10,
                           back_to_int=0)


@app.route("/showgithub/<select_id>/detail/<int:from_int>/<int:to_int>/")
def form_commits_for_projects_paging(select_id, from_int, to_int):
    selection_in_memory = GhSearchSelection.select().where(GhSearchSelection.id == select_id)
    return \
        render_template("detail.html",
                        commits=commits_selection_in_memory[from_int:to_int],
                        selection=selection_in_memory[0],
                        from_int=from_int + 10,
                        to_int=to_int + 10,
                        back_from_int=from_int - 10,
                        back_to_int=to_int - 10)


@app.route("/showgithub/<commit_id>/files/")
def files(commit_id):
    selections_with_mc = get_files(commit_id)
    return render_template("files.html", selections=selections_with_mc)


def get_files(commit_id):
    selections = FileChanges.select().where(FileChanges.id_commit == commit_id,
                                            FileChanges.extension.in_(['.ex', '.exs']))
    selections_with_mc_temp = []
    for sel in selections:
        analyse_text_after(sel)
        analyse_diff_text(sel)
        # if len(sel.diff_text_multicore_found) > 0:
        selections_with_mc_temp.append(sel)
    return selections_with_mc_temp


def analyse_text_after(sel):
    t = analyse(sel.text_after)
    sel.text_after_analysed = t[0]
    sel.multicore_found = t[1]


def analyse_diff_text(sel):
    t = analyse(sel.diff_text)
    sel.diff_text_analysed = t[0]
    sel.diff_text_multicore_found = t[1]


def analyse(text_to_analyse):
    i = 0
    text_after_analysed = ""
    found_mc = ""
    try:
        for line in text_to_analyse.splitlines():
            text = is_what(line)
            if len(text) > 0:
                found_mc = found_mc + "{} {} \n".format(i, text)
            text_after_analysed = text_after_analysed + "{} {}\n".format(i, line)
            i = i + 1
        return text_after_analysed, found_mc
    except AttributeError:
        return "", ""


def is_what(text):
    try:
        index_comment = text.index("#")
    except ValueError:
        index_comment = len(text)
    remarks = ""
    for f in functions:
        try:
            found_index = text.index(f)
        except ValueError:
            found_index = -1
        if 0 < found_index < index_comment:
            remarks = remarks + f

    return remarks


functions = ["spawn",
             "spawn_link",
             "spawn_monitor",
             "self",
             "send",
             "receive",
             "Agent",
             "Application",
             "Config",
             "Config.Provider",
             "Config.Reader",
             "DynamicSupervisor",
             "GenServer",
             "Node",
             "Process",
             "Registry",
             "Supervisor",
             "Task",
             "Task.Supervisor"]
