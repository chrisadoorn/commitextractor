import os
from flask import Flask, render_template, request, jsonify
from src.models.models import Project, CommitInfo, BestandsWijziging, ManualChecking

POSTGRESQL = 'postgresql'
CONFIGFILE = 'config.ini'
APP_DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/selected/")
def form_gh_search():
    ghs = Project.select().where(Project.main_language == "Elixir").order_by(Project.id.asc())
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


@app.route("/showgithub/<select_id>/commitsonly/")
def form_commits_only__for_projects(select_id):
    commits = CommitInfo.select().where(CommitInfo.idproject == select_id)
    for commit in commits:
        commit.selections_with_mc = get_files_info(commit.id)
    ghs: Project = Project.select().where(Project.id == select_id)
    return render_template("detail_commits.html",
                           commits=commits,
                           selection=ghs[0])


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


@app.route('/manual_comments/save/', methods=['POST', 'GET'])
def manual_comments():
    if request.method == 'POST':
        project_id = request.form['idproject']
        existing_manual_checking = ManualChecking.select().where(ManualChecking.idproject == project_id)
        if len(existing_manual_checking) == 0:
            manual_checking = ManualChecking()
            manual_checking.idproject = request.form['idproject']
            manual_checking.comment = request.form['comment']
            manual_checking.type_of_project = request.form['type_of_project']
            if 'exclude' in request.form:
                manual_checking.exclude = request.form['exclude']
            else:
                manual_checking.exclude = False
            manual_checking.exclude_reason = request.form['exclude_reason']
        else:
            manual_checking = existing_manual_checking[0]
            manual_checking.comment = request.form['comment']
            manual_checking.type_of_project = request.form['type_of_project']
            if 'exclude' in request.form:
                manual_checking.exclude = request.form['exclude']
            else:
                manual_checking.exclude = False
            manual_checking.exclude_reason = request.form['exclude_reason']
        manual_checking.save()
        return jsonify(status=201)
    else:
        project_id = request.args.get('mc_id')
        existing_manual_checking = ManualChecking.select().where(ManualChecking.idproject == project_id)
        if len(existing_manual_checking) == 0:
            manual_checking = ManualChecking()
            manual_checking.idproject = project_id
            manual_checking.comment = ''
            manual_checking.type_of_project = ''
            manual_checking.exclude = ''
            manual_checking.exclude_reason = ''
        else:
            manual_checking = existing_manual_checking[0]

        return jsonify(
            idproject=manual_checking.idproject_id,
            comment=manual_checking.comment,
            type_of_project=manual_checking.type_of_project,
            exclude=manual_checking.exclude,
            exclude_reason=manual_checking.exclude_reason
        )


def get_files(commit_id):
    selections = BestandsWijziging.select().where(BestandsWijziging.idcommit == commit_id)
    selections_with_mc_temp = []
    for sel in selections:
        analyse_text_after(sel)
        analyse_diff_text(sel)
        # if len(sel.diff_text_multicore_found) > 0:
        selections_with_mc_temp.append(sel)
    return selections_with_mc_temp


def get_files_info(commit_id):
    selections = BestandsWijziging.select().where(BestandsWijziging.idcommit == commit_id)
    selections_with_mc_temp = []
    for sel in selections:
        selections_with_mc_temp.append(sel)
        analyse_diff_text(sel)
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
