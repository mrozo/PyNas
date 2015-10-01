from Disk import Disk
from Partition import Partition
from ShellCmdWrapper import set_root_password

__author__ = 'm'


class ConfigParser:
    """
    Class designed to parse and verify config of the PyNas application. Read the
    documentation to check how the config has to be constructed
    """

    # todo make documentation

    __doc__ += """
    :var Config: raw structure of the config.
    :var Disks: frozenset containing Disk objects representing Disks section
                from the config.
    :var Partitions: list containing Partition objects representing
                     'Partitions' section of the config
    """
    Config = None
    Disks = list()
    Partitions = list()

    def __init__(self, config):
        """
        Initialize the instance and parse the config.
        :param config: data structure containing PyNas configuration.
        :return:
        """
        self.Config = config
        set_root_password(self.Config['RootPassword'])
        self.parse_disks()
        self.parse_partitions()

    def parse_disks(self):
        """
        Parse 'Disks' section from the config. Every disk record has to contain
        the following attributes : ['Name','SerialNumber','Type']
        """
        disks_list = []

        for disk_config in self.Config['Disks']:
            disk = Disk(SerialNumber=disk_config['SerialNumber'])
            disks_list.append(disk)

        self.Disks = disks_list

    def parse_partitions(self):
        """
        Parse 'Partitions' section from the config. Every partition record must
        contain the following attributes: ['Name', 'UUID', 'Disk', 'Type',
        'Required']
        """
        for disk in self.Disks:
            for partition in self.Config['Partitions']:
                if disk.Name == partition['Disk']:
                    pass

# todo create set of tests
