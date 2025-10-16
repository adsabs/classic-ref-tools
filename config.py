# -*- coding: utf-8 -*-
# ============================= LOGGING ======================================== #
LOGGING_LEVEL = 'INFO'
LOG_STDOUT = False
# ============================= ADS ============================================ #
ADS_API_TOKEN = "<secret>"
ADS_API_URL = "https://ui.adsabs.harvard.edu/v1"
# ============================= APPLICATION ==================================== #
# db config
SQLALCHEMY_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
# possible values: WARN, INFO, DEBUG
LOGGING_LEVEL = 'DEBUG'
LOG_STDOUT = False
# SQL queries for pipeline database
SQL_QUERIES = {
    'resolved':'SELECT DISTINCT processed_history.bibcode AS citing, resolved_reference.bibcode AS cited FROM processed_history JOIN resolved_reference ON processed_history.id=resolved_reference.history_id WHERE resolved_reference.score=1',
    'resolved_old':'SELECT processed_history.bibcode AS citing, resolved_reference.bibcode AS cited FROM processed_history JOIN resolved_reference ON processed_history.id=resolved_reference.history_id WHERE resolved_reference.score=1',
    'files':"SELECT DISTINCT source_filename, source_modified, date FROM processed_history WHERE {0} BETWEEN '{1}' AND '{2}'",
    'citing':"SELECT source_filename AS source_file, source_modified AS file_modified, date AS process_date  FROM processed_history WHERE processed_history.bibcode='{0}'",
    'cited':"SELECT processed_history.source_filename AS source_file, processed_history.source_modified AS file_modified, processed_history.date AS process_date  FROM processed_history JOIN resolved_reference ON processed_history.id=resolved_reference.history_id WHERE resolved_reference.score=1 AND resolved_reference.bibcode='{0}'",
    'text':"SELECT processed_history.bibcode AS citing, resolved_reference.reference_raw AS refstring, resolved_reference.score AS score FROM processed_history JOIN resolved_reference ON processed_history.id=resolved_reference.history_id WHERE UPPER(resolved_reference.reference_raw) LIKE '%{0}%'",
    'compare':"SELECT compare_classic.bibcode AS classic_bibcode, compare_classic.score AS classic_score, resolved_reference.bibcode AS service_bibcode, resolved_reference.score AS service_score, resolved_reference.reference_str AS refstr FROM compare_classic JOIN resolved_reference ON compare_classic.history_id=resolved_reference.history_id  AND compare_classic.item_num=resolved_reference.item_num WHERE compare_classic.state='{0}'",
}
# Header definitions
HEADER = {
    'files':'source file',
    'citing':'file\tmodified\tprocessed',
    'cited':'file\tmodified\tprocessed',
    'text':'citing_bibcode\trefstring\tservice_score',
    'compare':'classic_bibcode\tclassic_score\tservice_bibcode\tservice_score\trefstr',
}
# File and directory locations
RESOLVED_DIR='/proj/ads/references/links/pipeline'
CLASSIC_DIR = '/proj/ads/abstracts/config/links/reference'
COMPARISON_DIR = '/proj/ads/abstracts/config/links/reference'
