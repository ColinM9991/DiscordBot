import models.dcsserverinfo
import os
import psutil as psutil
import re
import socket
import subprocess
from slpp import slpp as lua


class DcsServer:
    def __init__(self,
                 instance_name: str,
                 instance_path: str,
                 service_name: str):
        self.instance_name: str = instance_name
        self.profile_path: str = instance_path
        self.service_name: str = service_name
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
        server_settings = self.get_server_settings()
        list_start_index = server_settings['listStartIndex']

        mission = server_settings['missionList'][list_start_index]

        return mission

    def get_server_info(self) -> models.dcsserverinfo.DcsServerInfo:
        config_dict = self.get_server_settings()

        return models.dcsserverinfo.DcsServerInfo(config_dict['name'],
                                                  config_dict['password'],
                                                  socket.gethostbyname(
                                                      socket.gethostname()),
                                                  config_dict['port'],
                                                  self.is_running())

    def is_running(self) -> bool:
        process_id = self.get_process_id()

        return process_id in (p.pid for p in psutil.process_iter())

    def get_server_settings(self):
        server_settings = os.path.join(self.config_path, 'serverSettings.lua')
        with open(server_settings) as settings_file:
            file_contents = settings_file.read()
            server_settings_dict = lua.decode(f'{{{file_contents}}}')

        config_dict = server_settings_dict['cfg']
        return config_dict

    def stop(self):
        subprocess.call(['firedaemon', '--stop', self.service_name])

    def start(self):
        subprocess.call(['firedaemon', '--start', self.service_name])
