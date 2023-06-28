import os

# zet hier de naam van het schema
new_schema='pj3'

scriptdir = os.path.dirname(__file__)

print(str(scriptdir))
run_dir = os.path.realpath(os.path.join(scriptdir, '../temp'))
print(run_dir)
sql_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
print(sql_dir)

file_names = ['10_create_table_selectie.sql'
    , '11_create_table_project.sql'
    , '12_create_table_commitinfo.sql'
    , '13_create_table_bestandswijziging.sql'
    , '21_create_table_processor.sql'
    , '22_create_table_verwerk_project.sql'
    , '23_create_table_verwerking_geschiedenis.sql'
    , '24_create_trigger_verwerk_project.sql'
    , '31_create_procedure_registreer_processor.sql'
    , '32_create_procedure_deregistreer_processor.sql'
    , '33_create_procedure_registreer_verwerking.sql'
    , '34_create_procedure_verwerk_volgend_project.sql'
    , '41_create_table_zoekterm.sql'
    , '42_create_table_bestandswijziging_info.sql'
    , '43_create_table_bestandswijziging_zoekterm.sql'
    , '44_create_table_handmatige_check.sql'
    , '45_create_manualchecking.sql'
    , '51_create_table_java_zoekterm.sql'
    , '52_vulscript_java_zoekterm.sql'
    , '53_create_java_parser_selection_view.sql'
    , '54_create_table_java_parse_result.sql'
    , '55_create_view_compare_analysis.sql'
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
full.write('GRANT USAGE ON SCHEMA ' + new_schema + ' TO appl;\n')

full.write('SET SCHEMA \'' + new_schema + '\';\n')

for sql_file in file_names:
    f_path = os.path.realpath(os.path.join(sql_dir, './' + sql_file))
    org = open(f_path, 'rt')
    full.write('------------------------------------------------------------------------------\n')
    full.write('------------------------------------------------------------------------------\n')
    full.write('--script--' + sql_file + '---------------------\n')
    full.write('------------------------------------------------------------------------------\n')
    full.write('------------------------------------------------------------------------------\n')
    for line in org:
        full.write(line)
    org.close()

full.close()

