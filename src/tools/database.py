import sqlalchemy

from src.core.singleton import Singleton
from src.core.exceptions import DatabaseError
from src.tools.configuration import Configuration

class Database:
    __metaclass__ = Singleton

    CONNECTION = None
    SESSION = None

    def connect(self):
        engine = sqlalchemy.create_engine('mysql+pymysql://%s:%s@%s/%s' % (Configuration.database['user'], \
                                                                           Configuration.database['password'], \
                                                                           Configuration.database['host'], \
                                                                           Configuration.database['name']))
        
        try:
            self.CONNECTION = engine.connect()
            self.SESSION =  sqlalchemy.orm.sessionmaker(bind=engine)()
        except Exception as e:
            raise DatabaseError(e)