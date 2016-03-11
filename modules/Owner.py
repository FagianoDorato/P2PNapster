class Owner:
    ipv4 = None
    ipv6 = None
    port = None

    def __init__(self, ipv4, ipv6, port):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.port = port