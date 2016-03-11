class SharedFile:
    name = None
    md5 = None
    owners = None

    def __init__(self, name, md5, owners=None):
        self.name = name
        self.md5 = md5
        self.owners = owners

    def dump(self):
        return {'name': self.name, 'md5': self.md5}
