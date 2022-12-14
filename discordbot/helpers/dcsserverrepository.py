import os
import re

from helpers import DcsServer


class DcsServerRepository:
    def __init__(self,
                 profile_path: str,
                 fire_daemon_service_exports: str):
        dcs_server_instances = {}
        for file in os.listdir(fire_daemon_service_exports):
            if not file.endswith('.xml'):
                continue

            file_path = os.path.join(fire_daemon_service_exports, file)
            with open(file_path) as file_contents:
                contents = file_contents.read()
                instance = re.search(
                    '<Parameters>(?:[A-Za-z0-9- ]+)&quot;([A-Za-z0-9.]+)&quot;</Parameters>', contents).group(1)

                instance_name = '.'.join(str(instance).split('.')[1:])
                instance_path = os.path.join(profile_path, str(instance))
                service_name = file.replace('.xml', '')

            if not os.path.exists(instance_path):
                continue

            server = DcsServer(instance_name, instance_path, service_name)
            dcs_server_instances[instance_name] = server

        self.instances = dcs_server_instances

    def get_instance(self, instance_name) -> DcsServer:
        if instance_name not in self.instances:
            raise ValueError(f'{instance_name} is not a valid server instance')

        return self.instances[instance_name]

    def get_instance_names(self):
        return self.instances.keys()
