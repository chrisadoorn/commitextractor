import os

from src.utils import db_postgresql

scriptdir = os.path.dirname(__file__)

print(str(scriptdir))
run_dir = os.path.realpath(os.path.join(scriptdir, '../temp'))
print(run_dir)
sql_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
print(sql_dir)

new_schema = 'test'
file_names = ['10_create_table_selectie.sql'
    , '11_create_table_project.sql'
    , '12_create_table_commitinfo.sql'
    , '13_create_table_bestandswijziging.sql'
    , '21_create_table_processor.sql'
    , '21_create_table_processor.sql'
    , '22_create_table_verwerk_project.sql'
    , '23_create_table_verwerking_geschiedenis.sql'
    , '31_create_procedure_registreer_processor.sql'
    , '32_create_procedure_deregistreer_processor.sql'
    , '33_create_procedure_registreer_verwerking.sql'
    , '34_create_procedure_verwerk_volgend_project.sql'
    , '41_create_table_zoekterm.sql'
    , '42_create_table_bestandswijziging_info.sql'
    , '43_create_table_bestandswijziging_zoekterm.sql'
    , '44_create_table_handmatige_check.sql'
    , '51_create_table_java_zoekterm.sql'
              ]

os.makedirs(run_dir)
full_script = os.path.realpath(os.path.join(run_dir, './' + 'full_script.' + new_schema + '.sql'))
full = open(full_script, 'wt')
full.write('------------------------------------------------------------------------------\n')
full.write('------------------------------------------------------------------------------\n')
full.write('-------------------create schema  ' + new_schema + '--------------------------\n')
full.write('------------------------------------------------------------------------------\n')
full.write('------------------------------------------------------------------------------\n')
full.write('CREATE SCHEMA IF NOT EXISTS ' + new_schema + ' AUTHORIZATION appl;\n')
full.write('GRANT ALL ON SCHEMA ' + new_schema + ' TO appl;\n')

for sql_file in file_names:
    f_path = os.path.realpath(os.path.join(sql_dir, './' + sql_file))
    org = open(f_path, 'rt')
    n_path = os.path.realpath(os.path.join(run_dir, './' + sql_file))
    new = open(n_path, 'wt')
    full.write('------------------------------------------------------------------------------\n')
    full.write('------------------------------------------------------------------------------\n')
    full.write('--script--' + sql_file + '---------------------\n')
    full.write('------------------------------------------------------------------------------\n')
    full.write('------------------------------------------------------------------------------\n')
    for line in org:
        new.write(line.replace("'test'", "'" + new_schema + "'"))
        full.write(line.replace("'test'", "'" + new_schema + "'"))
    org.close()
    new.close()


full.close()
# #    os.remove(n_path)
#
#
# # os.rmdir(run_dir)
