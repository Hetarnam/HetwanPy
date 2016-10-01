from src.tools.database import Database

class Base:
	def __init__(self):
		self.session = Database().get_session()
		self.register_dofus_packets()

	