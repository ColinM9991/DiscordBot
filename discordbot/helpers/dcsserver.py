from models import DcsServerInfo
from slpp import slpp as lua

import os
import psutil as psutil
import re
import socket
import subprocess


class DcsServer:
    def __init__(self,
                 instance_name: str,
                 instance_path: str,
                 service_name: str):
        self.instance_name: str = instance_name
        self.profile_path: str = instance_path
        self.service_name: str = service_name
        self.missions_path: str = os.path.join(instance_path, 'Missions')
        self.config_path: str = os.path.join(instance_path, 'Config')

    @property
    def get_instance_name(self) -> str:
        return self.instance_name

    @property
    def get_service_name(self) -> str:
        return self.service_name

    def get_process_id(self) -> int:
        active_service = subprocess.run(['firedaemon',
                                         '--status',
                                         self.get_service_name,
                                         '--pid'],
                                        stdout=subprocess.PIPE)
        pid_match = re.search(
            'App PID: ([0-9]+)', str(active_service.stdout)).group(1)

        return int(pid_match)

    def get_mission(self) -> str:
        files = [os.path.join(self.missions_path, file) for file in os.listdir(
            self.missions_path) if file.endswith('.miz')]

        # A server must have only one mission file
        if len(files) < 1:
            raise ValueError('No missions found.')
        elif len(files) > 1:
            raise ValueError('Too many missions.')

        return files[0]

    def get_server_info(self) -> DcsServerInfo:
        server_settings = os.path.join(self.config_path, 'serverSettings.lua')
        with open(server_settings) as settings_file:
            file_contents = settings_file.read()
            server_settings_dict = lua.decode(f'{{{file_contents}}}')

        config_dict = server_settings_dict['cfg']

        return DcsServerInfo(config_dict['name'],
                             config_dict['password'],
                             socket.gethostbyname(socket.gethostname()),
                             config_dict['port'],
                             self.is_running())

    def is_running(self) -> bool:
        process_id = self.get_process_id()

        return process_id in (p.pid for p in psutil.process_iter())

    def stop(self):
        subprocess.call(['firedaemon', '--stop', self.service_name])

    def start(self):
        subprocess.call(['firedaemon', '--start', self.service_name])
