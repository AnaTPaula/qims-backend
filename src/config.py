import logging
from os import getenv

from connexion import App
from connexion.resolver import RestyResolver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from psycopg2 import connect, DatabaseError
from psycopg2.extras import DictCursor

from model.model import Base


class Config:
    def __init__(self):
        self.secret = 'kjasdhjwdiqw7121#$79*lacfkw*/'
        self.logging_level = None
        self.debug = None
        self.app = None
        self.database_url = None
        self.database_host = None
        self.database_username = None
        self.database_password = None
        self.database_port = None
        self.database_name = None

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
        self.database_host = 'localhost'
        self.database_username = 'postgres'
        self.database_password = 'postgres'
        self.database_port = '5432'
        self.database_name = 'qim'


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.port_host = 8000
        self.debug = False
        self.logging_level = logging.INFO
        # TODO: change it when configure prod environment.
        self.origin = 'http://localhost:4200'
        self.database_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/qim'
        self.database_host = 'localhost'
        self.database_username = 'postgres'
        self.database_password = 'postgres'
        self.database_port = '5432'
        self.database_name = 'qim'


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


class Database:
    def __init__(self, config: Config):
        self.host = config.database_host
        self.username = config.database_username
        self.password = config.database_password
        self.port = config.database_port
        self.db_name = config.database_name
        self.conn = None

    def get_connection(self):
        if self.conn is None:
            try:
                self.conn = connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    port=self.port,
                    dbname=self.db_name
                )
            except DatabaseError as e:
                logging.error(e)
                raise e

    def select_all(self, query):
        self.get_connection()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            records = [dict(row) for row in cur.fetchall()]
            cur.close()
            return records

    def select_one(self, query):
        self.get_connection()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            record = cur.fetchone()
            cur.close()
            return dict(record) if record else None

    def execute(self, query):
        try:
            self.get_connection()
            with self.conn.cursor() as cur:
                cur.execute(query)
                self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            cur.close()


database = Database(config=get_config())
