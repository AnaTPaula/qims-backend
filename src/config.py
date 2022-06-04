import logging
from os import getenv

from connexion import App
from connexion.resolver import RestyResolver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.model import Base


class Config:
    def __init__(self):
        self.secret = 'kjasdhjwdiqw7121#$79*lacfkw*/'
        self.logging_level = None
        self.debug = None
        self.app = None
        self.database_url = None

    def create_table(self):
        engine = self.__get_engine()
        Base.metadata.create_all(engine)

    def get_session(self):
        engine = self.__get_engine()
        Base.metadata.bind = engine
        return sessionmaker(bind=engine)()

    def __get_engine(self):
        return create_engine(self.database_url)


class Localconfig(Config):
    def __init__(self):
        super().__init__()
        self.port_host = 8000
        self.debug = True
        self.logging_level = logging.DEBUG
        self.origin = 'http://localhost:4200'
        self.database_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/qim'


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.port_host = 8000
        self.debug = False
        self.logging_level = logging.INFO
        # TODO: change it when configure prod environment.
        self.origin = 'http://localhost:4200'
        self.database_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/qim'


def get_config():
    env = getenv('ENV', 'local')
    return ProductionConfig() if 'prod' == env else Localconfig()


def config_application(config: Config):
    options = {'swagger_url': '/'}
    app = App(__name__, specification_dir='swagger/', options=options)
    app.add_api('v1.yaml', base_path='/v1', resolver=RestyResolver('controller'), strict_validation=False)
    app.secret_key = config.secret
    app.debug = config.debug
    return app
