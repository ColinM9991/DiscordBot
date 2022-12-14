import psutil as psutil


class DcsServer:
    def is_running(self):
        pass


class ConcreteDcsServer(DcsServer):
    def is_running(self):
        return "dcs" in (p.name() for p in psutil.process_iter())