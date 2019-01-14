import json
import datetime
import logging
import os

from api.config.default import Config


class ProductionConfig(Config):
    DEBUG = False

    SIGNATURE = True

    # SERVER
    SERVER_SCHEME = 'http'
    SERVER_DOMAIN = 'localhost:5000'

    # SQL
    PSQL_USER = ''
    PSQL_PASSWORD = ''
    PSQL_PORT = ''
    PSQL_DATABASE = ''
    PSQL_HOST = ''

    SQLALCHEMY_DATABASE_URI = os.environ.get('REDSHIFT_DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False

    # JWT
    SECRET_KEY = 'marathon'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # flask_cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_DB = '3'
