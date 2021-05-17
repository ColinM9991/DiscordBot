import models.dcsserverinfo
import os
import socket
from slpp import slpp as lua


class DcsServer:
    def __init__(self,
                 instance_name: str,
                 instance_path: str):
        self.__instance_name: str = instance_name
        self.__config_path: str = os.path.join(instance_path, 'Config')

    @property
    def get_instance_name(self) -> str:
        return self.__instance_name

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
                                                  config_dict['port'])

    def get_server_settings(self):
        server_settings = os.path.join(self.__config_path, 'serverSettings.lua')
        with open(server_settings) as settings_file:
            file_contents = settings_file.read()
            server_settings_dict = lua.decode(f'{{{file_contents}}}')

        config_dict = server_settings_dict['cfg']
        return config_dict