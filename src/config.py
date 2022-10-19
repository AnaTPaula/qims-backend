import logging
from os import getenv
from psycopg2 import connect, DatabaseError
from psycopg2.extras import DictCursor


class Config:
    def __init__(self):
        self.secret = getenv('SECRET', 'kjasdhjwdiqw7121#$79*lacfkw*/')
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
        with open('table.sql') as file:
            script = file.read()
        database.execute(script)


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
        self.port_host = 8080
        self.debug = False
        self.logging_level = logging.INFO
        self.origin = getenv('ORIGIN')
        self.database_host = getenv('RDS_HOSTNAME')
        self.database_username = getenv('RDS_USERNAME')
        self.database_password = getenv('RDS_PASSWORD')
        self.database_port = getenv('RDS_PORT')
        self.database_name = getenv('RDS_DB_NAME')


def get_config():
    env = getenv('ENV', 'local')
    return ProductionConfig() if 'prod' == env else Localconfig()


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

    def select_all(self, query: str, params: tuple = None):
        self.get_connection()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            records = [dict(row) for row in cur.fetchall()]
            cur.close()
            return records

    def select_one(self, query: str, params: tuple = None):
        self.get_connection()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            record = cur.fetchone()
            cur.close()
            return dict(record) if record else None

    def execute(self, query: str, params: tuple = None):
        try:
            self.get_connection()
            with self.conn.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            cur.close()

    def execute_returning_id(self, query: str, params: tuple = None):
        try:
            self.get_connection()
            with self.conn.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                self.conn.commit()
                return cur.fetchone()[0]
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            cur.close()


database = Database(config=get_config())
