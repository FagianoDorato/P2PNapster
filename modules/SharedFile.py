class SharedFile:
    name = None
    md5 = None

    def __init__(self, name, md5):
        self.name = name
        self.md5 = md5

    def dump(self):
        return {'name': self.name, 'md5': self.md5}
