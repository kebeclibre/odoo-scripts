#!/usr/bin/python3
import psycopg2
from psycopg2 import sql
from docopt import docopt
from pprint import pprint
import sys
import os
import shutil


doc = """
Usage:
    postgres.py clean_db [-d]
    postgres.py clean_fs [-d]
    postgres.py clean_all [-d]
    postgres.py clean_dumps [-d]

Options:
    -d, --dry-run    dry run
"""
DB_POSGRES = ['template0', 'template1', 'postgres', 'vmail']
DB_NO_CLEAN = DB_POSGRES + ['odoo-mock%']

STABLES = ['9.0', '10.0', '11.0', '12.0']
SAAS_INCLUDE = ['saas-[0-9]{2}.[0-2]?']
SAAS_EXCLUDE = ['saas-[1][1-2].[3-9]']


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
                    shutil.rmtree(to_delete)


def main():
    opt = docopt(doc)
    dry_run = False
    if opt.get('--dry-run'):
        pprint('DRYRUN')
        dry_run = True
    commands = Commands(dry_run)

    if opt.get('clean_db'):
        commands.clean_databases()
    if opt.get('clean_fs'):
        commands.clean_dir_tree('filestore')
    if opt.get('clean_dumps'):
        commands.clean_dir_tree('dumps')
    if opt.get('clean_all'):
        commands.clean_databases()
        commands.clean_dir_tree(False)

    sys.exit(0)


if __name__ == '__main__':
    main()
