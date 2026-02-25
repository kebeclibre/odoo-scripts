#!/usr/bin/python3
import argparse
import psycopg2
from psycopg2 import sql
from pprint import pprint
import sys
import os
import shutil

DB_POSGRES = ['template0', 'template1', 'postgres', 'vmail']
DB_NO_CLEAN = DB_POSGRES + ['odoo-mock%']

STABLES = ['18.0', '19.0']
SAAS_INCLUDE = ['saas-[0-9]{2}.[0-2]?']
SAAS_EXCLUDE = ['saas-[1][3].[3-9]']


DIRS_TO_CLEAN = {
    'filestore': '/home/odoo/.local/share/Odoo/filestore',
    'dumps': '/home/odoo/devel/DUMPS',
}


class Connection(object):
    def __init__(self, autocommit=False):
        self.autocommit = autocommit
        self.conn = psycopg2.connect("dbname=postgres user=odoo")
        self.cr = self.conn.cursor()
        self.set_session(autocommit=self.autocommit)

    def close(self):
        if self.cr:
            self.cr.close()
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def __getattr__(self, item):
        if hasattr(self.cr, item):
            return getattr(self.cr, item)
        if hasattr(self.conn, item):
            return getattr(self.conn, item)

    def execute(self, query, params):
        try:
            self.cr.execute(query, params)
        except Exception as e:
            pprint('EXEC Exception %s' % e)
            self.rollback()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


class Commands(object):

    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def _get_databases_to_clean(self):
        include_db = SAAS_INCLUDE

        query_params = {'exclude': '|'.join(STABLES + DB_NO_CLEAN + SAAS_EXCLUDE)}
        query = '''
            SELECT datname FROM pg_database
                WHERE datname NOT SIMILAR TO %(exclude)s '''
        if include_db:
            query_params['include'] = '|'.join(include_db)
            query += '''OR datname SIMILAR TO %(include)s'''

        with Connection() as conn:
            conn.execute(query, query_params)
            db_to_delete = conn.fetchall()

        return [db[0] for db in db_to_delete]

    def clean_databases(self):
        query = sql.SQL('DROP DATABASE ')
        query_params = (None, )
        db_to_delete = self._get_databases_to_clean()
        with Connection(autocommit=True) as conn:
            for db in db_to_delete:
                composed_query = sql.Composed([query, sql.Identifier(db)])
                query_string = composed_query.as_string(conn.cr)
                if self.dry_run:
                    pprint(conn.mogrify(query_string, query_params))
                else:
                    conn.execute(query_string, query_params)

    def clean_dir_tree(self, tree='filestore'):
        if not tree:
            to_delete = DIRS_TO_CLEAN
        else:
            to_delete = {tree: DIRS_TO_CLEAN[tree]}

        for key, path in to_delete.items():
            file_stores = os.listdir(path)

            for store in file_stores:
                to_delete = '/'.join([path, store])
                if self.dry_run:
                    pprint(to_delete)
                else:
                    if os.path.isfile(to_delete):
                        os.remove(to_delete)
                    else:
                        shutil.rmtree(to_delete)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["clean_db", "clean_fs", "clean_dumps", "clean_all"])
    parser.add_argument("--true-run", required=False, action="store_true")
    args = parser.parse_args()
    dry_run = not args.true_run
    if dry_run:
        pprint('DRYRUN')
    commands = Commands(dry_run)

    command = args.command
    match command:
        case 'clean_db':
            commands.clean_databases()
        case 'clean_fs':
            commands.clean_dir_tree('filestore')
        case 'clean_dumps':
            commands.clean_dir_tree('dumps')
        case'clean_all':
            commands.clean_databases()
            commands.clean_dir_tree(False)

    sys.exit(0)


if __name__ == '__main__':
    main()
