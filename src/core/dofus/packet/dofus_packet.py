import logging, re
from src.core.singleton import Singleton


class DofusPacket:
	__metaclass__ = Singleton

	_list = {}

	@classmethod
	def register_packets(cls):
		for packet in [packet for packet in dir(cls) if str(packet).startswith('DofusPacket')]:
			dofus_packet = getattr(cls, packet)(cls)

			DofusPacket().register(dofus_packet.FORMAT, dofus_packet)

	def register(self, packet_format, handler):
		if packet_format not in self._list:
			self._list.update({packet_format: handler})

	def handle(self, packet, socket_client):
		logging.debug('(%s@%d) Packet received : %s', socket_client.client_address[0], socket_client.client_address[1], format(packet))
		for packet_format, handler in self._list.iteritems():
			if re.match(packet_format, packet):
				return handler.handle(handler.parse(packet), socket_client)
		logging.warning('Unable to handle packet : %s', format(packet))
		return None

class DofusPacketHandler:
	DESCRIPTION = 'Dofus packet'
	FORMAT = None

	def __init__(self, model=None):
		self.model = model

	@staticmethod
	def parse(packet):
		return packet

	def handle(self, packet, socket_client):
		pass