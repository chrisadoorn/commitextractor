import os

from flask import Flask, render_template

from src.models.models import Project, CommitInfo, BestandsWijziging

POSTGRESQL = 'postgresql'
CONFIGFILE = 'config.ini'
APP_DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def form_gh_search():
    ghs = Project.select()
    return render_template("selected.html", latest_selection_list=ghs)


@app.route("/showgithub/<select_id>/detail/")
def form_commits_for_projects(select_id):
    commits = CommitInfo.select().where(CommitInfo.idproject == select_id)
    ghs: Project = Project.select().where(Project.id == select_id)
    for commit in commits[0:10]:
        commit.selections_with_mc = get_files(commit.id)
    return render_template("detail.html",
                           commits=commits[0:10],
                           selection=ghs[0],
                           from_int=10,
                           to_int=20,
                           back_from_int=-10,
                           back_to_int=0)


@app.route("/showgithub/<select_id>/detail/<int:from_int>/<int:to_int>/")
def form_commits_for_projects_paging(select_id, from_int=0, to_int=10):
    commits = CommitInfo.select().where(CommitInfo.idproject == select_id)
    ghs: Project = Project.select().where(Project.id == select_id)
    for commit in commits[from_int:to_int]:
        commit.selections_with_mc = get_files(commit.id)
    return \
        render_template("detail.html",
                        commits=commits[from_int:to_int],
                        selection=ghs[0],
                        from_int=from_int + 10,
                        to_int=to_int + 10,
                        back_from_int=from_int - 10,
                        back_to_int=to_int - 10)


def get_files(commit_id):
    selections = BestandsWijziging.select().where(BestandsWijziging.idcommit == commit_id)
    selections_with_mc_temp = []
    for sel in selections:
        analyse_text_after(sel)
        analyse_diff_text(sel)
        # if len(sel.diff_text_multicore_found) > 0:
        selections_with_mc_temp.append(sel)
    return selections_with_mc_temp


def analyse_text_after(sel):
    t = analyse(sel.tekstachteraf)
    sel.text_after_analysed = t[0]
    sel.multicore_found = t[1]


def analyse_diff_text(sel):
    t = analyse(sel.difftext)
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
