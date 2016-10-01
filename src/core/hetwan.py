import logging, sys

from enum import Enum

from src.network.login.login_server import LoginServer
from src.tools.database import Database
from src.tools.configuration import Configuration

from .exceptions import ConfigurationError, DatabaseError

class Core:
	class EmulatorStates(Enum):
		IN_LOADING = 0
		IN_RUNNING = 1
		IN_CLOSING = 2

	state = None

	def __init__(self):
		Core.state = self.EmulatorStates.IN_LOADING

		logging.basicConfig(format = '(%(asctime)s) [%(levelname)s] %(message)s', datefmt = '%a, %d %b %Y %H:%M:%S', level = logging.DEBUG)

		try:
			logging.info('Loading configuration file...')
			Configuration('config.yml')
			logging.debug('Configuration file loaded!')
			logging.info('Connection to database...')
			Database().connect()
			logging.debug('Connected!')
			logging.debug('Loading finished!')
		except (ConfigurationError, DatabaseError) as e:
			logging.error('Error on loading: %s' % format(e))
			sys.exit()

	def start(self):
		Core.state = self.EmulatorStates.IN_RUNNING

		try:
			logging.info('Creating socket server...')
			socket_server = LoginServer()
			logging.debug('Shhhhhttt ! Listening for some connections...')
			socket_server.start()
		except Exception as e:
			logging.error('Error on running: %s' % format(e))
		finally:
			sys.exit()