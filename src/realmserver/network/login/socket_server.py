import socket, threading, logging, sys
from client_thread import ClientThread

class SocketServer:
	CLIENTS = list()

	def __init__(self, server_ip, server_port, max_connections):
		try:
			self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.tcpsock.bind((server_ip, server_port))
			self.tcpsock.listen(10)

			logging.info('Socket server successfully started !')
		except Exception as e:
			logging.error(format(e))

	def start(self):
		from src.realmserver.core.hetwan import EmulatorState, Core

		while (Core.STATE == EmulatorState.IN_RUNNING):
			try:
				(clientsock, (ip, port)) = self.tcpsock.accept()
				new_client = ClientThread(len(self.CLIENTS), ip, port, clientsock)
				self.CLIENTS.append(new_client)
				new_client.start()
			except Exception as e:
				print format(e)

		for client in self.CLIENTS:
			client.join()