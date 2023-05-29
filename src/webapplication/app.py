from flask import Flask, render_template, request, jsonify

from src.models.analyzed_data_models import Zoekterm
from src.models.extracted_data_models import CommitInfo, BestandsWijziging
from src.models.selection_models import Project, pg_db_schema, pg_db
from src.models.webapp_models import ManualChecking, Handmatige_Check
from src.utils import configurator
from src.utils.read_diff import ReadDiff

app = Flask(__name__)
app.config.from_object(__name__)
language = configurator.get_main_language()[0]
readDiff = ReadDiff(language=language)

zoektermen = [x.zoekwoord for x in Zoekterm.select(Zoekterm.zoekwoord).distinct()]


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/selected/")
def form_gh_search():
    ghs = Project.select().order_by(Project.id.asc())
    return render_template("selected.html", latest_selection_list=ghs)


@app.route("/showgithub/<select_id>/detail/")
def form_commits_for_projects(select_id):
    try:
        sql = "select ci.id, ci.commitdatumtijd, ci.author_id, ci.remark  " \
              "from {sch}.commitinfo as ci where ci.idproject = {idproject} " \
              "and ci.id in " \
              "(select bw.idcommit from {sch}.bestandswijziging as bw " \
              "where bw.extensie != '.md') " \
              "limit {li} offset {os};".format(sch=pg_db_schema, li=10, os=0, idproject=select_id)
        cursor = pg_db.execute_sql(sql)
        ghs: Project = Project.select().where(Project.id == select_id)
        commits: list[any] = []
        for (id1, commitdatumtijd, author_id, remark) in cursor.fetchall():
            selections_with_mc = analyse_diff(id1)
            print(selections_with_mc)
            commits.append((id1, commitdatumtijd, author_id, remark, selections_with_mc))
        return render_template("detail.html", commits=commits, selection=ghs[0], from_int=10, to_int=20,
                               back_from_int=-10, back_to_int=0)
    except Exception as e:
        print(e)


@app.route("/showgithub/<select_id>/change/<false_positive>/")
def form_changes_for_projects(select_id, false_positive):
    try:
        sql = "select hc.bwz_id, hc.zoekterm, hc.falsepositive, hc.regelnummers, hc.bestandswijziging_id, " \
              "hc.commit_datum, hc.commit_remark, hc.commit_sha, hc.gecontroleerd, hc.akkoord, hc.opmerking, hc.id  " \
              "from {sch}.handmatige_check hc " \
              "where hc.falsepositive = {false_positive} " \
              "and hc.project_id = {idproject} " \
              "limit {li} offset {os};".format(sch=pg_db_schema, li=1, os=0, idproject=select_id,
                                               false_positive=false_positive)
        cursor = pg_db.execute_sql(sql)
        ghs: Project = Project.select().where(Project.id == select_id)
        commits: list[any] = []
        for (bz_id, zoekterm, falsepositive, regelnummers, idbestandswijziging, commitdatumtijd,
             remark, hashvalue, gecontroleerd, akkoord, opmerking, id) in cursor.fetchall():
            selections_with_mc = analyse_diff_by_bwid(idbestandswijziging)
            print(selections_with_mc)
            commits.append((bz_id, zoekterm, falsepositive, regelnummers, idbestandswijziging, commitdatumtijd, remark,
                            hashvalue, gecontroleerd, akkoord, opmerking, id, selections_with_mc))
        return render_template("change.html", commits=commits, selection=ghs[0], from_int=1, to_int=2,
                               back_from_int=-1, back_to_int=0, false_positive=false_positive)
    except Exception as e:
        print(e)


@app.route("/showgithub/<select_id>/change/<int:from_int>/<int:to_int>/<false_positive>/")
def form_changes_for_projects_paging(select_id, from_int=0, to_int=1, false_positive='false'):
    sql = "select hc.bwz_id, hc.zoekterm, hc.falsepositive, hc.regelnummers, hc.bestandswijziging_id, " \
          "hc.commit_datum, hc.commit_remark, hc.commit_sha, hc.gecontroleerd, hc.akkoord, hc.opmerking, hc.id  " \
          "from {sch}.handmatige_check hc " \
          "where hc.falsepositive = {false_positive} " \
          "and hc.project_id = {idproject} " \
          "limit {li} offset {os};".format(sch=pg_db_schema, li=to_int - from_int, os=from_int,
                                           idproject=select_id, false_positive=false_positive)
    cursor = pg_db.execute_sql(sql)
    ghs: Project = Project.select().where(Project.id == select_id)
    commits: list[any] = []
    for (
            bz_id, zoekterm, falsepositive, regelnummers, idbestandswijziging, commitdatumtijd,
            remark, hashvalue, gecontroleerd, akkoord, opmerking, id) in cursor.fetchall():
        selections_with_mc = analyse_diff_by_bwid(idbestandswijziging)
        print(selections_with_mc)
        commits.append((bz_id, zoekterm, falsepositive, regelnummers, idbestandswijziging, commitdatumtijd, remark,
                        hashvalue, gecontroleerd, akkoord, opmerking, id, selections_with_mc))
    return render_template("change.html", commits=commits, selection=ghs[0], from_int=from_int + 1, to_int=to_int + 1,
                           back_from_int=from_int - 1, back_to_int=to_int - 1, false_positive=false_positive)


@app.route('/change/save/', methods=['POST'])
def change_check():
    table_id = int(request.form.get('table_id', 0))
    akkoord = bool(request.form.get('akkoord', False))
    opmerking = request.form.get('opmerking', '')
    handmatige_check = Handmatige_Check.select().where(Handmatige_Check.id == table_id)[0]
    handmatige_check.gecontroleerd = True
    handmatige_check.akkoord = akkoord
    handmatige_check.opmerking = opmerking
    handmatige_check.save()
    return jsonify(status=201)


@app.route("/showgithub/<select_id>/commitsonly/")
def form_commits_only__for_projects(select_id):
    commits = CommitInfo.select().where(CommitInfo.idproject == select_id)
    ghs: Project = Project.select().where(Project.id == select_id)
    return render_template("detail_commits.html", commits=commits, selection=ghs[0])


@app.route("/showgithub/<select_id>/detail/<int:from_int>/<int:to_int>/")
def form_commits_for_projects_paging(select_id, from_int=0, to_int=10):
    sql = "select ci.id, ci.commitdatumtijd, ci.author_id, ci.remark  " \
          "from {sch}.commitinfo as ci where ci.idproject = {idproject} " \
          "and ci.id in " \
          "(select bw.idcommit from {sch}.bestandswijziging as bw " \
          "where (bw.extensie == '.java' or bw.extensie == '.exs' or bw.extensie == '.ex' or bw.extensie == '.rs') " \
          "limit {li} offset {os};".format(sch=pg_db_schema, li=to_int - from_int, os=from_int, idproject=select_id)
    cursor = pg_db.execute_sql(sql)
    ghs: Project = Project.select().where(Project.id == select_id)
    commits: list[any] = []
    for (id1, commitdatumtijd, author_id, remark) in cursor.fetchall():
        selections_with_mc = analyse_diff(id1)
        commits.append((id1, commitdatumtijd, author_id, remark, selections_with_mc))

    return render_template("detail.html", commits=commits, selection=ghs[0], from_int=from_int + 10, to_int=to_int + 10,
                           back_from_int=from_int - 10, back_to_int=to_int - 10)


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

        return jsonify(idproject=manual_checking.idproject_id, comment=manual_checking.comment,
                       type_of_project=manual_checking.type_of_project, exclude=manual_checking.exclude,
                       exclude_reason=manual_checking.exclude_reason)


def bestandswijzigingen_to_list(selections):
    selections_list = []
    try:
        for sel in selections:
            nl_netto, ol1 = readDiff.check_diff_text(sel.difftext, zoektermen)
            nl, ol2 = readDiff.check_diff_text_no_check_with_removed(sel.difftext, zoektermen)
            sel.diff_netto = create_string(nl_netto)
            sel.diff_ol = create_string(ol2)
            sel.diff_nl = create_string(nl)
            sel.simple_search = simple_search(sel.tekstachteraf)
            sel.tekstachteraf = add_line_numbers(sel.tekstachteraf)
            selections_list.append(sel)
        return selections_list
    except Exception as e:
        print(e)


def add_line_numbers(text: str):
    if text is None:
        return ''
    lines = text.splitlines()
    for i in range(len(lines)):
        lines[i] = str(i + 1) + ' :' + lines[i]
    return '\n'.join(lines)


def simple_search(text: str):
    if text is None:
        return []
    lines = text.splitlines()
    result = []
    for i in range(len(lines)):
        regel = lines[i]
        for z in zoektermen:
            if z in regel:
                result.append((i + 1, z))

    return result


def analyse_diff(commit_id):
    selections = BestandsWijziging.select().where(BestandsWijziging.idcommit == commit_id,
                                                  BestandsWijziging.extensie != '.md')
    return bestandswijzigingen_to_list(selections)


def analyse_diff_by_bwid(bestandswijziging_id):
    selections = BestandsWijziging.select().where(BestandsWijziging.id == bestandswijziging_id)
    return bestandswijzigingen_to_list(selections)


def create_string(input_list: list[tuple[int, str, [str]]]) -> str:
    string = ''
    for (ln, l, k) in input_list:
        if len(k) > 0:
            string += 'Line ' + str(ln) + ', mc words:' + str(k) + '\n'
    return string
