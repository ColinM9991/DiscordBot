class DcsServerInfo:
    server_name: str
    password: str
    ip_address: str
    port: int

    def __init__(self,
                 server_name: str,
                 password: str,
                 ip_address: str,
                 port: int):
        self.server_name = server_name
        self.password = password
        self.ip_address = ip_address
        self.port = port
