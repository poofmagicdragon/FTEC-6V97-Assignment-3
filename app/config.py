database_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'kiwirootdb',
    'database': 'kiwilocal'
}

import os 

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{database_config.get('user')}:{database_config.get('password')}@{database_config.get('host')}:{database_config.get('port')}/{database_config.get('database')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    Debug = False