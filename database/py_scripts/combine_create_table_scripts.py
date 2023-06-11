import os


def create_database_script(new_schema='refact'):
    scriptdir = os.path.dirname(__file__)

    print(str(scriptdir))
    run_dir = os.path.realpath(os.path.join(scriptdir, '../temp'))
    print(run_dir)
    sql_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    print(sql_dir)

    file_names = ['10_create_table_selectie.sql', '11_create_table_project.sql', '12_create_table_commitinfo.sql',
                  '13_create_table_bestandswijziging.sql', '21_create_table_processor.sql',
                  '21_create_table_processor.sql', '22_create_table_verwerk_project.sql',
                  '23_create_table_verwerking_geschiedenis.sql', '31_create_procedure_registreer_processor.sql',
                  '32_create_procedure_deregistreer_processor.sql', '33_create_procedure_registreer_verwerking.sql',
                  '34_create_procedure_verwerk_volgend_project.sql', '41_create_table_zoekterm.sql',
                  '42_create_table_bestandswijziging_info.sql', '43_create_table_bestandswijziging_zoekterm.sql',
                  '44_create_table_handmatige_check.sql', '45_create_manualchecking.sql',
                  '51_create_table_java_zoekterm.sql']

    os.makedirs(run_dir)
    full_script = os.path.realpath(os.path.join(run_dir, './' + 'full_script.' + new_schema + '.sql'))
    full = open(full_script, 'wt')
    full.write('------------------------------------------------------------------------------\n')
    full.write('------------------------------------------------------------------------------\n')
    full.write('-------------------create schema  ' + new_schema + '--------------------------\n')
    full.write('------------------------------------------------------------------------------\n')
    full.write('------------------------------------------------------------------------------\n')
    full.write('CREATE SCHEMA IF NOT EXISTS ' + new_schema + ';\n')
    full.write('SET SCHEMA \'' + new_schema + '\';\n')

    for sql_file in file_names:
        f_path = os.path.realpath(os.path.join(sql_dir, './' + sql_file))
        org = open(f_path, 'rt')
        org_text = read_file(f_path).splitlines()
        org.close()
        full.write('------------------------------------------------------------------------------\n')
        full.write('------------------------------------------------------------------------------\n')
        full.write('--script--' + sql_file + '---------------------\n')
        full.write('------------------------------------------------------------------------------\n')
        full.write('------------------------------------------------------------------------------\n')
        start_write = False
        is_procedure = False
        for line in org_text:
            line = line.replace('bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 )', 'BIGSERIAL')
            line_temp = line.strip()
            if line_temp and line.startswith(')'):
                full.write(');\n')
                full.write('\n')
                start_write = False
                continue
            if line_temp.startswith('CREATE TABLE') or line_temp.startswith('CREATE INDEX'):
                start_write = True
            if line_temp.startswith('ALTER TABLE') and 'ADD CONSTRAINT' in line_temp:
                start_write = True
                line = line.replace('_fk', '_fk_' + new_schema)
            if line_temp.startswith('CREATE OR REPLACE PROCEDURE'):
                start_write = True
                is_procedure = True
            if line_temp.startswith('set schema'):
                continue
            if start_write:
                full.write(line + '\n')
            if is_procedure and line_temp.startswith('$BODY$;'):
                start_write = False
                is_procedure = False
            if not is_procedure and line_temp.endswith(';'):
                start_write = False
    full.close()


def read_file(filepath):
    file = open(filepath, 'rt')
    text = file.read()
    file.close()
    return text


if __name__ == '__main__':
    create_database_script('v3')
    print("Aanmaken create database script gestart.")
