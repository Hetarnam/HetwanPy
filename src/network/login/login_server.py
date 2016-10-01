import SocketServer, threading, random, re, string

from sqlalchemy.orm.exc import NoResultFound

from src.core.dofus.packet.dofus_packet import DofusPacket, DofusPacketHandler

from src.models.user import User

from src.tools.configuration import Configuration
from src.tools.database import Database

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
	def __init__(self, request, client_address, server):
		self.DofusPackets()
		self.key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))

		SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

	class DofusPackets(DofusPacket):
		def __init__(self):
			self.register_packets()

		class DofusPacketConnection(DofusPacketHandler):
			FORMAT = '(\w+)#(\w+)'

			@staticmethod
			def parse(packet):
				parsed = packet.split('#')
				
				return (parsed[0], parsed[1])

			def handle(self, (username, password), socket_client):
				try:
					user = Database().get_session().query(User).filter(User.username == username).one()

					if User.encrypt_password(user.password, socket_client.key) != password:
						raise NoResultFound
				except NoResultFound:
					socket_client.send('AlEf') # wrong password packet

	def handle(self):
		print 'new client!'

		self.send('HC%s' % self.key)

		while True:
			packets = [packet for packet in re.split(r"\s|\x00", self.request.recv(4096).replace("\n", '')) if bool(packet.strip()) is True]

			if not packets:
				break
			for packet in packets:
				DofusPacket().handle(packet, self)

		print 'client is gone'
		self.request.close()

	def send(self, packet):
		self.request.send('%s\x00' % packet)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class LoginServer:
	_clients = []

	def __init__(self):
		self.server = ThreadedTCPServer((Configuration().communication['dofus_client']['ip'], \
										 Configuration().communication['dofus_client']['port']), \
										ThreadedTCPRequestHandler)

	def start(self):
		server_thread = threading.Thread(target=self.server.serve_forever)
		server_thread.start()