class DcsServerInfo:
    server_name: str
    password: str
    ip_address: str
    port: int
    is_active: bool

    def __init__(
        self,
        server_name: str,
        password: str,
        ip_address: str,
        port: int,
        is_active: bool,
    ):
        self.server_name = server_name
        self.password = password
        self.ip_address = ip_address
        self.port = port
        self.is_active = is_active
