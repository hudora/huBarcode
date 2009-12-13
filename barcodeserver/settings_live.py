#!/usr/bin/python
# Django settings for MoftS production use.

from settings import *

DATABASE_ENGINE = 'postgresql_psycopg2' # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'dbname'       # Or path to database file if using sqlite3.
DATABASE_USER = 'user'         # Not used with sqlite3. # webserver
DATABASE_PASSWORD = 'geheim'   # Not used with sqlite3. # zimZity
DATABASE_HOST = '0.0.0.0'      # Set to empty string for localhost. Not used with sqlite3.

DEBUG = False
