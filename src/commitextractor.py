from datetime import datetime
from pydriller import Repository
from src import db_postgresql
from src.db_postgresql import get_connection

# pip install package pydriller
# pip install package mysql-connector-python


# reponaam = 'https://github.com/ishepard/pydriller'
# reponaam = '/git/android/ou-mini-bieb'
# reponaam = '/git/java/nifi'
reponaam = 'https://github.com/chrisadoorn/OUwebclient'

commit_teller = 0
start = datetime.now()
print(start)
vandaagMySqlFormat = start.strftime("%Y-%m-%d")

connectie = get_connection()

new_id = 0
val = (reponaam, 'Java', new_id)

projectId = db_postgresql.insert_project(connectie, val)
print("project " + reponaam + " inserted with id: " + str(projectId))

exit(7)

fullRepository = Repository(reponaam)
commit_teller = 0
for commit in fullRepository.traverse_commits():
    commit_teller = commit_teller + 1

    commitcursor = connectie.cursor()
    commit_datetime = commit.committer_date
    commitMySqlFormat = commit_datetime.strftime("%Y-%m-%d %H:%M:%S")
    commit_remark = commit.msg[:200]  # limit the comment
    sql = "INSERT INTO tests.commit(datum, hashvalue, username, emailadress, remark, idproject) VALUES (%s, %s, %s, %s, %s, %s);"
    val_commit = (commitMySqlFormat, commit.hash, commit.author.name, commit.author.email, commit_remark, projectId)
    commitcursor.execute(sql, val_commit)
    commitId = commitcursor.lastrowid
    print('commit: ' + str(commit_teller))

    for file in commit.modified_files:
        print(file.filename, ' has changed')
        if not (file.filename.endswith('.zip') or file.filename.endswith('.eot') or file.filename.endswith(
                '.woff') or file.filename.endswith('interface.saveScore.loadScore.txt')):
            # sla op in database
            filecursor = connectie.cursor()

            sql = "INSERT INTO tests.bestandswijziging (tekstvooraf, tekstachteraf, verschil, locatie, idcommit) VALUES (%s, %s, %s, %s, %s)"
            val = (file.content_before, file.content, file.diff, file.new_path, commitId)
            filecursor.execute(sql, val)
            rowId = filecursor.lastrowid
            connectie.commit()

#          print(filecursor.rowcount, "record inserted with id: " + str(rowId))

print("aantal commits : " + str(commit_teller))

eind = datetime.now()
print(eind)
duur = eind - start
print(duur)
