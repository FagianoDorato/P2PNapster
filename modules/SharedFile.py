class SharedFile:
	name = None
	md5 = None
	shared = None

	def __init__(self, name, md5, shared):
		self.name = name
		self.md5 = md5
		self.shared = shared

	def dump(self):
		return {'name': self.name, 'md5': self.md5, 'shared': self.shared}

