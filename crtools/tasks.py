from __future__ import absolute_import, unicode_literals
import os
import sys
from builtins import str
from collections import defaultdict
import crtools.app as app_module
from crtools.utils import get_resolved
from crtools.utils import get_files
from crtools.utils import get_refdata
from crtools.exceptions import PipelineExportFailure
# ============================= INITIALIZATION ==================================== #

from adsputils import setup_logging, load_config

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
config = load_config(proj_home=proj_home)
app = app_module.crtools('ads-classic-ref-tools', proj_home=proj_home, local_config=globals().get('local_config', {}))
logger = app.logger
# ============================= FUNCTIONS ========================================= #
def export_resolved_references(**args):
    ref_source = 'ads'
    if args['refsource']:
        ref_source = args['refsource']
    output_file = "{0}/pipeline_{1}_refs.dat".format(config['RESOLVED_DIR'],ref_source)
    try:
        resolved = get_resolved(src=ref_source)
    except Exception as e:
        logger.error('Failed to get resolved references from pipeline database: {0}'.format(str(e)))
        raise PipelineExportFailure('Failed to get resolved references from pipeline database: {0}'.format(str(e)))

    # Output is a list of tuples
    with open(output_file, 'w') as fp:
        fp.write('\n'.join('{}\t{}'.format(x[0],x[1]) for x in resolved))
        fp.write('\n')

def show_files(**args):
    dtypes = {
        'processed':'date',
        'updated':'source_modified'
    }
    start_date = args.get('start_date', None)
    end_date = args.get('end_date', None)
    dtype = args.get('dtype', None)
    date_type = dtypes.get(dtype, None)
    bibcode = args.get('bibcode')
    relation= args.get('relation')

    try:
        file_list = get_files(dtype=date_type, sd=start_date, ed=end_date, bibcode=bibcode, relation=relation)
    except Exception as e:
        logger.error('Failed to retrieve file list from pipeline database: {0}'.format(str(e)))
        raise PipelineExportFailure('Failed to retrieve file list from pipeline database: {0}'.format(str(e)))

    if dtype:
        print(config['HEADER']['files'])
    else:
        print(config['HEADER'][relation])

    for entry in file_list:
        print("{0}\t{1}\t{2}".format(entry[0], entry[1].strftime("%Y-%m-%d"), entry[2].strftime("%Y-%m-%d")))

def search_refdata(txt):
    try:
        results = get_refdata(txt)
    except Exception as e:
        logger.error('Failed to retrieve references list from pipeline database: {0}'.format(str(e)))
        raise PipelineExportFailure('Failed to retrieve references list from pipeline database: {0}'.format(str(e)))

    print(config['HEADER']['text'])
    for entry in results:
        print("{0}\t{1}\t{2}".format(entry[0], entry[1], entry[2]))

def compare_classic(state):
    try:
        results = get_refdata(state, qtype='compare')
    except Exception as e:
        logger.error('Failed to retrieve classic comparison data from pipeline database: {0}'.format(str(e)))
        raise PipelineExportFailure('Failed to retrieve classic comparison data from pipeline database: {0}'.format(str(e)))

    print(config['HEADER']['compare'])
    for entry in results:
        print("{0}\t{1}\t{2}\t{3}\t{4}".format(entry[0], entry[1], entry[2], entry[3], entry[4]))

def compare_pipeline_classic(**args):
    ref_source = 'ads'
    if args['refsource']:
        ref_source = args['refsource']

    counts_file = '{0}/pipeline_classic_comparison_{1}.tsv'.format(config['COMPARISON_DIR'], ref_source)

    if ref_source == 'ads':
        classic_file = '{0}/{1}_refs.dat'.format(config['CLASSIC_DIR'], ref_source.lower())
    else:
        classic_file = '{0}/{1}_refs.tab'.format(config['CLASSIC_DIR'], ref_source.lower())
    if not os.path.exists(classic_file):
        sys.exit('Unable to find file with Classic references: {0}'.format(classic_file))
    if ref_source == 'ads':
        pipeline_file= '{0}/pipeline_{1}_refs.dat'.format(config['CLASSIC_DIR'], ref_source.lower())
    else:
        pipeline_file= '{0}/pipeline_{1}_refs.tab'.format(config['CLASSIC_DIR'], ref_source.lower())
    if not os.path.exists(pipeline_file):
        sys.exit('Unable to find file with Pipeline references: {0}'.format(pipeline_file))

    # We want to output results for all unique preprint bibcodes in both files
    # If a bibcode is in one but not the other, we will print 0 for the amount
    # of references found for that bibcode in that file
    citbibs = set()
    # Get the counts for the Classic results
    # This can probably be done more efficiently (we need this just during the transition)
    classic_counts = defaultdict(int)
    with open(classic_file) as cf:
        for line in cf:
            citing, cited = line.strip().split('\t')
            classic_counts[citing] += 1
            citbibs.add(citing)

    # Get the counts for the pipeline results
    # These can also be retrieved from the pipeline DB
    pipeline_counts = defaultdict(int)
    with open(pipeline_file) as cf:
        for line in cf:
            citing, cited = line.strip().split('\t')
            pipeline_counts[citing] += 1
            citbibs.add(citing)

    with open(counts_file,'w') as cf:
        for bibcode in citbibs:
            cf.write('{0}\t{1}\t{2}\n'.format(bibcode, classic_counts.get(bibcode, 0), pipeline_counts.get(bibcode, 0)))
