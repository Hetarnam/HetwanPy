import socket, threading, logging, sys

from .client_thread import ClientThread

class SocketServer:
	_clients = list()

	def __init__(self, server_ip, server_port, max_connections):
		try:
			self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.tcpsock.bind((server_ip, server_port))
			self.tcpsock.listen(10)

			logging.info('Socket server successfully created!')
		except Exception as e:
			logging.error(format(e))

	def start(self):
		from src.core.hetwan import Core

		id = 0

		while (Core.state == Core.EmulatorStates.IN_RUNNING):
			try:
				(clientsock, (ip, port)) = self.tcpsock.accept()
				new_client = ClientThread(id, ip, port, clientsock)
				self._clients.append(new_client)
				new_client.start()

				id += 1
			except Exception as e:
				print format(e)

		for client in self._clients:
			client.join()