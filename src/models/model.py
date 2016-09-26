class BaseModel:
	def register_dofus_packets(self):
		for packet in [packet for packet in dir(self) if str(packet).startswith('DofusPacket')]:
			getattr(self, packet)(self).register()