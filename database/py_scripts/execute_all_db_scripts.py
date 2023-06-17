import os

from peewee import *
from psycopg2 import OperationalError

from src.utils import configurator


def create_database_script(new_schema):
    sql_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    file_names = ['10_create_table_selectie.sql', '11_create_table_project.sql', '12_create_table_commitinfo.sql',
                  '13_create_table_bestandswijziging.sql', '21_create_table_processor.sql',
                  '21_create_table_processor.sql', '22_create_table_verwerk_project.sql',
                  '23_create_table_verwerking_geschiedenis.sql', '31_create_procedure_registreer_processor.sql',
                  '32_create_procedure_deregistreer_processor.sql', '33_create_procedure_registreer_verwerking.sql',
                  '34_create_procedure_verwerk_volgend_project.sql', '41_create_table_zoekterm.sql',
                  '42_create_table_bestandswijziging_info.sql', '43_create_table_bestandswijziging_zoekterm.sql',
                  '44_create_table_handmatige_check.sql', '45_create_manualchecking.sql',
                  '51_create_table_java_zoekterm.sql']

    full_script = 'CREATE SCHEMA IF NOT EXISTS ' + new_schema + ';\n'
    full_script = full_script + 'SET SCHEMA \'' + new_schema + '\';\n'

    for sql_file in file_names:
        f_path = os.path.realpath(os.path.join(sql_dir, './' + sql_file))
        org_text = read_file(f_path).splitlines()
        start_write = False
        is_procedure = False
        full_script = full_script + '--script--' + sql_file + '---------------------\n'
        for line in org_text:
            line_temp = line.strip()
            if line_temp and line.startswith(')'):
                full_script = full_script + ');\n'
                full_script = full_script + '\n'
                start_write = False
                continue
            if line_temp.startswith('CREATE TABLE'):
                start_write = True
                if not ("IF NOT EXISTS" in line_temp):
                    line = line_temp.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
            if line_temp.startswith('CREATE INDEX'):
                start_write = True
                if not ("IF NOT EXISTS" in line_temp):
                    line = line_temp.replace("CREATE INDEX", "CREATE INDEX IF NOT EXISTS")
            if line_temp.startswith('CREATE OR REPLACE PROCEDURE'):
                start_write = True
                is_procedure = True
            if start_write:
                full_script = full_script + line + '\n'
            if is_procedure and line_temp.startswith('$BODY$;'):
                start_write = False
                is_procedure = False
            if not is_procedure and line_temp.endswith(';'):
                start_write = False
    return full_script


def execute_script(script_text):
    try:
        params_for_db = configurator.get_database_configuration()
        connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'),
                                        password=params_for_db.get('password'), host='localhost',
                                        port=params_for_db.get('port'))
        connection.execute_sql(script_text)

    except OperationalError:
        print("Error connecting to the database :/")

    finally:
        if connection:
            connection.close()
            print("Closed connection.")


def read_file(filepath):
    file = open(filepath, 'rt')
    text = file.read()
    file.close()
    return text


if __name__ == '__main__':
    print("Database script gestart.")
    schema_name = 'v3'
    script = create_database_script(schema_name)
    execute_script(script)
    print("Database script uitgevoerd.")
