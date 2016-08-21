import logging
from src.realmserver.network.login.socket_server import SocketServer

class EmulatorState:
	IN_LOADING = 0
	IN_RUNNING = 1
	IN_CLOSING = 2

class Core:
	STATE = -1

	def __init__(self):
		logging.basicConfig(
			format = '(%(asctime)s) [%(levelname)s] %(message)s',
			datefmt = '%a, %d %b %Y %H:%M:%S',
			level = logging.DEBUG
		)

		Core.STATE = EmulatorState.IN_LOADING
		logging.info('HetwanPy emulator for Dofus %s', '1.29.1')

	def start(self):
		Core.STATE = EmulatorState.IN_RUNNING
		logging.debug('Creating socket server...')
		socket_server = SocketServer('127.0.0.1', 444, 10)
		logging.debug('Shhhhhhhhhhhhhttt ! Listen for some connections...')
		socket_server.start()