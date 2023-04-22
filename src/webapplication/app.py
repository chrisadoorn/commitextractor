from flask import Flask, render_template, request, jsonify

from src.models.models import Project, CommitInfo, BestandsWijziging, ManualChecking
from src.utils import configurator
from src.utils.read_diff import ReadDiff, Language

app = Flask(__name__)
app.config.from_object(__name__)
language = configurator.get_main_language()[0]

readDiff = ReadDiff(language=Language[language.upper()])

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/selected/")
def form_gh_search():
    ghs = Project.select().order_by(Project.id.asc())
    return render_template("selected.html", latest_selection_list=ghs)


@app.route("/showgithub/<select_id>/detail/")
def form_commits_for_projects(select_id):
    commits = CommitInfo.select().where(CommitInfo.idproject == select_id)
    ghs: Project = Project.select().where(Project.id == select_id)
    for commit in commits[0:10]:
        commit.selections_with_mc = analyse_diff(commit.id)
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
    ghs: Project = Project.select().where(Project.id == select_id)
    return render_template("detail_commits.html",
                           commits=commits,
                           selection=ghs[0])


@app.route("/showgithub/<select_id>/detail/<int:from_int>/<int:to_int>/")
def form_commits_for_projects_paging(select_id, from_int=0, to_int=10):
    commits = CommitInfo.select().where(CommitInfo.idproject == select_id)
    project: Project = Project.select().where(Project.id == select_id)
    for commit in commits[from_int:to_int]:
        commit.selections_with_mc = analyse_diff(commit.id)
    return \
        render_template("detail.html",
                        commits=commits[from_int:to_int],
                        selection=project[0],
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


def analyse_diff(commit_id):
    selections = BestandsWijziging.select().where(BestandsWijziging.idcommit == commit_id,
                                                  BestandsWijziging.extensie != '.md')
    selections_with_mc_temp = []
    for sel in selections:
        dif = readDiff.read_diff_text(sel.difftext)
        sel.diff_nl = create_string(dif[0])
        sel.diff_ol = create_string(dif[1])
        selections_with_mc_temp.append(sel)
    return selections_with_mc_temp


def create_string(input_list: list[tuple[int, str, [str]]]) -> str:
    string = ''
    return string.join([str(ln) + ':' + l + ':' + str(k) + '\n' for (ln, l, k) in input_list])














