from .dofus_packet import DofusPacket


class DofusPacketHandler:
	DESCRIPTION = 'Dofus packet'
	FORMAT = None

	def __init__(self, model):
		self.model = model

	def register(self):
		DofusPacket.register(self.FORMAT, self.handle)

	def handle(self, packet):
		print '%s: handled !' % self.FORMAT, self.model
		pass