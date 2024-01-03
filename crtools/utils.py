import os
import sys
import psycopg2

# ============================= INITIALIZATION ==================================== #

from adsputils import setup_logging, load_config

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
config = load_config(proj_home=proj_home)

def do_query(sql):
    pg_connection_dict = {
    'database': config.get('_DB_NAME'),
    'user': config.get('_DB_USER'),
    'password': config.get('_DB_PWD'),
    'port': config.get('_DB_PORT'),
    'host': config.get('_DB_HOST')
}

    conn = psycopg2.connect(**pg_connection_dict)
    cursor = conn.cursor()

    cursor.execute('''{0}'''.format(sql))
    rows = cursor.fetchall();
    conn.close()

    return rows

def get_resolved(**args):

    query = config['SQL_QUERIES']['resolved']
    results = do_query(query)
    return results

def get_files(**args):

    if args['dtype']:
        query = config['SQL_QUERIES']['files'].format(args['dtype'], args['sd'], args['ed'])
    elif args['relation']:
        query = config['SQL_QUERIES'][args['relation']].format(args['bibcode'])
    results = do_query(query)
    return results

def get_refdata(s, qtype='text'):
    query = config['SQL_QUERIES'][qtype].format(s.upper())
    results = do_query(query)
    return results
