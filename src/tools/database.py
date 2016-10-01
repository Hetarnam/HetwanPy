import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base

from src.core.singleton import Singleton
from src.core.exceptions import DatabaseError
from src.tools.configuration import Configuration

Base = declarative_base()

class Database:
    __metaclass__ = Singleton

    CONNECTION = None
    engine = None

    def connect(self):
        self.engine = sqlalchemy.create_engine('mysql+pymysql://%s:%s@%s/%s' % (Configuration.database['user'], \
                                                                           Configuration.database['password'], \
                                                                           Configuration.database['host'], \
                                                                           Configuration.database['name']))
        
        try:
            self.CONNECTION = self.engine.connect()
        except Exception as e:
            raise DatabaseError(e)

    def get_session(self):
        return sqlalchemy.orm.sessionmaker(bind=self.engine)()