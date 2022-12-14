import psutil as psutil


class DcsServer:
    def is_running(self):
        return "dcs" in (p.name() for p in psutil.process_iter())