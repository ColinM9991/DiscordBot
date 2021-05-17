import os
import re
import subprocess
import helpers.dcsserver
import wmi


class DcsServerRepository:
    def __init__(self, profile_path: str, service_names):
        self.service_names = service_names
        dcs_server_instances = {}

        wmi_query = wmi.WMI()
        for process in wmi_query.Win32_Process(name="DCS.exe"):
            instance_name = re.search(
                '-w \"([A-Za-z0-9.]+)\"', process.CommandLine).group(1)
            instance_path = os.path.join(profile_path, instance_name)

            if not os.path.exists(instance_path):
                continue

            server = helpers.dcsserver.DcsServer(instance_name, instance_path)
            dcs_server_instances[instance_name] = server

        self.instances = dcs_server_instances

    def get_instance(self, instance_name) -> helpers.dcsserver.DcsServer:
        if instance_name not in self.instances:
            raise ValueError(f'{instance_name} is not a valid server instance')

        return self.instances[instance_name]

    def get_instance_names(self):
        return self.instances.keys()

    def stop(self, instance_name):
        self.invoke_core(instance_name, 'stop')

    def start(self, instance_name):
        self.invoke_core(instance_name, 'start')

    def invoke_core(self, instance_name, action):
        if instance_name not in self.instances or instance_name not in self.service_names:
            return

        subprocess.call(
            ['firedaemon', f'--{action}', self.service_names[instance_name]])
