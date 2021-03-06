import threading, logging, string, random, re

from src.models.user.user import User

class ClientThread(threading.Thread):
	def __init__(self, client_id, client_ip, client_port, socket):
		threading.Thread.__init__(self)

		self.key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
		self.client_id = client_id
		self.client_ip = client_ip
		self.client_port = client_port
		self.socket = socket

		logging.debug('(%d) Client join us !', client_id)

	def run(self):
		self.send('HC%s' % self.key)

		while True:
			entry = re.split(r"\s+", self.socket.recv(4096).replace("\n", ''))

			if not entry:
				break
			for packet in entry:
				logging.debug('(%d) Packet received : %s', self.client_id, str(packet))

		self.kill()

	def send(self, packet):
		return self.socket.send("%s\x00" % packet)

	def kill(self):
		self.socket.close()
		logging.debug('(%d) Client is gone...', self.client_id)