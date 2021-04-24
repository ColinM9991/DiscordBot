import os
import psutil as psutil
import re
import subprocess


class DcsServer:
    def __init__(self, instance_name, instance_path, service_name):
        self.instance_name = instance_name
        self.profile_path = instance_path
        self.service_name = service_name
        self.missions_path = os.path.join(instance_path, 'Missions')

    @property
    def get_instance_name(self) -> str:
        self.instance_name

    @property
    def get_service_name(self) -> str:
        return self.service_name

    def get_process_id(self) -> int:
        active_service = subprocess.run(['firedaemon',
                                         '--status',
                                         self.get_service_name,
                                         '--pid'],
                                        stdout=subprocess.PIPE)
        pid_match = re.search('App PID: ([0-9]+)', str(active_service.stdout)).group(1)

        return int(pid_match)

    def get_mission(self) -> str:
        files = [os.path.join(self.missions_path, file) for file in os.listdir(self.missions_path) if file.endswith('.miz')]

        # A server must have only one mission file
        if len(files) < 1:
            return
        elif len(files) > 1:
            return

        return files[0]

    def is_running(self):
        process_id = self.get_process_id()
        print(f'Process ID is {process_id}')

        return process_id in (p.pid for p in psutil.process_iter())

    def stop(self):
        subprocess.call(['firedaemon', '--stop', self.service_name])

    def start(self):
        subprocess.call(['firedaemon', '--start', self.service_name])


class MultiInstanceDcsServer:
    def __init__(self, profile_path, fire_daemon_service_exports):
        dcs_server_instances = {}
        for file in os.listdir(fire_daemon_service_exports):
            if not file.endswith('.xml'):
                continue

            file_path = os.path.join(fire_daemon_service_exports, file)
            with open(file_path) as file_contents:
                contents = file_contents.read()
                instance = re.search('<Parameters>(?:[A-Za-z0-9- ]+)&quot;([A-Za-z0-9.]+)&quot;</Parameters>', contents).group(1)

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

    def get_instances(self):
        return self.instances.keys()
