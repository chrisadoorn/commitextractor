from app import app
from src.models.models import *
# from src.models.models import GhSearchSelection, CommitInformation, FileChanges


def create_tables():
    pg_db.create_tables([GhSearchSelection, CommitInformation, FileChanges], safe=True)


if __name__ == '__main__':
    create_tables()
    app.run()
