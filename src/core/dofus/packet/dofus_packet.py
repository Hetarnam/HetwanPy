import re


class DofusPacket:
	_list = {}

	@classmethod
	def register(self, format, handler):
		self._list.update({format: handler})

	@classmethod
	def handle(self, packet):
		for format, handler in self._list.iteritems():
			if re.match(format, packet):
				return handler(packet)
		return None