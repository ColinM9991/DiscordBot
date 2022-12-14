import psutil as psutil
import os


class DcsServer:
    def __init__(self, profile_path, instances):
        self.profile_path = profile_path
        self.instances = instances

    def is_running(self):
        pass

    def get_instances(self):
        pass

    def get_mission(self, instance_path):
        pass


class ConcreteDcsServer(DcsServer):
    def __init__(self, profile_path):
        super().__init__(profile_path, [folder for folder in os.listdir(profile_path) if(folder.startswith('DCS.'))])

    def is_running(self):
        return "dcs" in (p.name() for p in psutil.process_iter())

    def get_instances(self):
        instance_names = ['.'.join(folder.split('.')[1:]) for folder in self.instances]

        return instance_names

    def get_mission(self, instance_name):
        if instance_name is None:
            raise ValueError('Instance name must be specified.')

        instance_path = next(folder_path for folder_path in self.instances if instance_name in folder_path)
        if instance_path is None:
            raise ValueError('Invalid instance name specified')

        mission_directory = os.path.join(self.profile_path, instance_path, 'Missions')
        if not os.path.exists(mission_directory):
            raise ValueError(f'{instance_name} is not a valid instance')

        mission_files = [os.path.join(mission_directory, file) for file in os.listdir(mission_directory) if (os.path.isfile(os.path.join(mission_directory, file)) and file.endswith('.miz'))]
        if len(mission_files) > 1:
            return

        return mission_files[0]
