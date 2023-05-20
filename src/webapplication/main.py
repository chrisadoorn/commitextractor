from app import app
from src.models.models import pg_db, ManualChecking


def create_table_if_not_exists():
    pg_db.create_tables(
        [ManualChecking],
        safe=True)


if __name__ == '__main__':
  #  create_table_if_not_exists()
    app.run()
