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
# File locations
RESOLVED_FILE = '/tmp'
