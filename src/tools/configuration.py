import yaml

from src.core.singleton import Singleton
from src.core.exceptions import ConfigurationError

class Configuration:
    __metaclass__ = Singleton

    dofus = {'version': '127.0.0.1', 'enable_subscription': False}
    communication = {'dofus_client': {'ip': '127.0.0.1', 'port': 444}}
    database = {'host': '127.0.0.1', 'user': 'root', 'password': None, 'name': None}

    def __init__(self, file_path):
        with open(file_path, 'r') as stream:
            try:
                self.read(yaml.load(stream))
            except yaml.YAMLError as e:
                raise ConfigurationError(e)

    def read(self, content):
        try:
            self.dofus['version'] = content['dofus_version']
            self.dofus['enable_subscription'] = content['dofus_enable_subscription']

            self.communication['dofus_client']['ip'] = content['communication']['dofus_client']['ip']
            self.communication['dofus_client']['port'] = content['communication']['dofus_client']['port']

            self.database['host'] = content['database']['host']
            self.database['user'] = content['database']['user']
            self.database['password'] = content['database']['password']
            self.database['name'] = content['database']['name']
        except Exception as var:
            raise ConfigurationError('Unable to find %s in configuration file' % var)