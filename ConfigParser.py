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

        for partition_config in self.Config['Partitions']:

            partition = Partition(
                UUID=partition_config['UUID'],
                Name=partition_config['Name'],
                Filesystem=partition_config['Type'],
                Required=partition_config['Required']
            )
            self.Partitions.append(partition)

            for disk in self.Disks:
                if disk.Name == partition_config['Disk']:
                    disk.Partitions.append(partition)



# todo create set of tests

def config_parser_class_tests():
    from copy import deepcopy

    partition1 = Partition(
        Name="partition1",
        UUID="0123456789ABCDEF",
        Filesystem="EXT4"
    )
    partition2 = Partition(
        Name="partition12",
        UUID="fedcba0987654321",
        Filesystem="EXT4"
    )
    partition3 = Partition(
        Name="partition13",
        UUID="0101010101010101",
        Filesystem="NTFS"
    )
    new_partition = Partition(
        Name="newPartition",
        UUID="2222222222222222",
        Filesystem="EXT2"
    )
    hd1 = Disk(
        SerialNumber="hitachi11111",
        Partitions=[partition1, partition2],
        Name="hitachi66666"
    )
    hd2 = Disk(
        SerialNumber="hd2",
        Partitions=[partition3, partition2, new_partition],
        Name="hd2"
    )

    config_src = {
        "RootPassword": 'k',
        "Disks": [
            {"Name": "hd1", "SerialNumber": "hitachi11111", "Type": "Sata"},
            {"Name": "hd2", "SerialNumber": "hitachi66666", "Type": "Sata"},
        ],
        "Partitions": [
            {"Name": "partition1", "UUID": "0123456789ABCDEF", "Disk": "hd1",
             "Type": "EXT4", "Required": True},
            {"Name": "partition2", "UUID": "fedcba0987654321", "Disk": "hd1",
             "Type": "EXT4", "Required": True},
            {"Name": "partition3", "UUID": "0101010101010101", "Disk": "hd2",
             "Type": "NTFS", "Required": True},
            {"Name": "newPartition", "UUID": "2222222222222222", "Disk": "hd2",
             "Type": "EXT2", "Required": True},
        ]
    }

    broken_config_src = deepcopy(config_src)
    broken_config_src['Partitions'].append(
        {"Name": "partition4", "UUID": "9999999999999999", "Disk": "hd1",
         "Type": "EXT4", "Required": True}
    )
    broken_config_src['Disks'].append(
        {"Name": "hd3", "SerialNumber": "123234345311", "Type": "Sata"}
    )

    try:
        config = ConfigParser(config_src)
    except Exception as E:
        assert False, 'Failed to parse a proper config\n' + str(E)

    try:
        broken_config = ConfigParser(broken_config_src)
    except Exception as E:
        assert False, 'Failed to parse the config with a bad data\n' + str(E)

    assert len(config.Partitions) == 4, "Failed to parse properly partitions " \
                                        "from the config len(config." \
                                        "Partitions) equals " + \
                                        str(len(config.Partitions)) + \
                                        ", should be 4"

    assert len(config.Disks) == 2, "Failed to properly parse Disks from the " \
                                   "config. len(config.Disks) equals " +\
                                   str(len(config.Disks)) + ", should be 2"

    assert len(broken_config.Partitions) == 5, "Failed to properly parse " \
                                               "partitions in the broken_config" \
                                               ". len(broken_config.Partitions)" \
                                               " equals " + \
                                               str(len(broken_config.Partitions)) + \
                                               ", should be 5"

    assert len(broken_config.Disks) == 3, "Failed to properly parse Disks from"\
                                          " the broken_config. " + \
                                          "len(broken_config.Partitions) equals"\
                                          + " " + str(len(broken_config.Disks))\
                                          + ", should be 3 "

    # todo len(config.Disks[x].partitions) for every disk
    return True


