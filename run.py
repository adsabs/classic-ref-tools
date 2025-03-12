from __future__ import print_function
import argparse
import sys
import os
from datetime import datetime, timedelta
from crtools import tasks

# ============================= INITIALIZATION ==================================== #

from adsputils import setup_logging, load_config
proj_home = os.path.realpath(os.path.dirname(__file__))
config = load_config(proj_home=proj_home)
logger = setup_logging('run.py', proj_home=proj_home,
                        level=config.get('LOGGING_LEVEL', 'INFO'),
                        attach_stdout=config.get('LOG_STDOUT', False))
                        

# =============================== FUNCTIONS ======================================= #

def_end_date = datetime.now().strftime("%Y-%m-%d")
def_start_date = (datetime.now() - timedelta(days=31)).strftime("%Y-%m-%d")
 
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--resolved', action="store_true",
                        help='Export citing/cited pairs for resolved references')
    parser.add_argument('-rs', '--source', default=False, dest='ref_source',
                        help='Set source for references')
    parser.add_argument('-d', '--date', default=False, dest='date',
                        help='Show files that were processed/updated')
    parser.add_argument('-sd', '--start_date', default=def_start_date, dest='start_date',
                        help='Start date of period')
    parser.add_argument('-ed', '--end_date', default=def_end_date, dest='end_date',
                        help='Start date of period')
    parser.add_argument('-s', '--citing', default=False, dest='citing',
                        help='Show files for citing bibcode')
    parser.add_argument('-t', '--cited', default=False, dest='cited',
                        help='Show files for cited bibcode')
    parser.add_argument('-x', '--text', default=False, dest='text',
                        help='Show reference strings containing text')
    parser.add_argument('-c', '--check', default=False, dest='check',
                        help='Show results of checking with Classic')
    parser.add_argument('-cmp', '--comparison',  action="store_true",
                        help='Save Classic and pipeline counts to file')
    args = parser.parse_args()

    if args.resolved:
        results = tasks.export_resolved_references(refsource=args.ref_source)
    elif args.date:
        # If no start date is provided, the default is to get files from the past month
        results = tasks.show_files(dtype=args.date, start_date=args.start_date, end_date=args.end_date)
#        print("Show files that were: {0}".format(args.date))
    elif args.citing:
        results = tasks.show_files(bibcode=args.citing, relation='citing')
#        print("Show files for citing bibcode: {0}".format(args.citing))
    elif args.cited:
        results = tasks.show_files(bibcode=args.cited, relation='cited')
#        print("Show files for cited bibcode: {0}".format(args.cited))
    elif args.text:
        results = tasks.search_refdata(args.text)
#        print("Show references with text: {0}".format(args.text))
    elif args.check:
        results = tasks.compare_classic(args.check)
        print("Show references with check status: {0}".format(args.check))
    elif args.comparison:
        results = tasks.compare_pipeline_classic(refsource=args.ref_source)
    else:
        sys.exit("No comprendo")
