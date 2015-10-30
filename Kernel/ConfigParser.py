from Hardware.Disk import Disk
from Hardware.Partition import Partition
from Wrappers.ShellCmdWrapper import set_root_password
from Kernel.Exceptions import *

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
    Disks = None
    Partitions = None

    def __init__(self, config):
        """
        Initialize the instance and parse the config.
        :param config: data structure containing PyNas configuration.
        """
        self.Partitions = list()
        self.Disks = list()
        self.Config = config
        set_root_password(self.Config['RootPassword'])
        self.parse_disks()
        self.parse_partitions()

    def parse_disks(self):
        """
        Parse 'Disks' section from the config
        """

        for disk_config in self.Config['Disks']:
            disk = Disk(
                Name=disk_config['Name'],
                SerialNumber=disk_config['SerialNumber']
            )
            self.Disks.append(disk)


    def parse_partitions(self):
        """
        Parse 'Partitions' section from the config
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

                    if disk.Partitions is None:
                        disk.Partitions = list()

                    disk.Partitions.append(partition)
                    break
            else:
                raise MissingDeviceError()


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
    partition4 = Partition(
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
        Partitions=[partition3, partition4],
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
            {"Name": "partition4", "UUID": "2222222222222222", "Disk": "hd2",
             "Type": "EXT2", "Required": True},
        ]
    }

    #
    # create the broken_config_src by copying the config_src and appending
    # some wrong data
    #
    broken_config_src = deepcopy(config_src)
    broken_config_src['Partitions'].append(
        {"Name": "newPartition", "UUID": "9999999999999999", "Disk": "hd3",
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

    #
    # Test if partitions section from config_src and broken_config_src have been
    # properly parsed
    #
    assert len(config.Partitions) == 4, """
Failed to parse properly partitions from the config len(config.Partitions)
equals """ + str(len(config.Partitions)) + """, should be 4.
"""

    assert len(broken_config.Partitions) == 5, """
Failed to properly parse partitions in the broken_config. len(broken_config.Partitions)
equals """ + str(len(broken_config.Partitions)) + """, should be 5.
"""

    #
    # Test if disks section from config_src and broken_config_src have been
    # properly parsed
    #
    assert len(config.Disks) == 2, """
Failed to properly parse Disks from the config. len(config.Disks) equals
""" + str(len(config.Disks)) + """, should be 2.
"""
    assert len(broken_config.Disks) == 3, """
Failed to properly parse Disks from the broken_config. len(broken_config.Partitions)
equals """ + str(len(broken_config.Disks)) + """, should be 3.
"""

    #
    # Test if partitions have been assigned to a proper hard drives during
    # parsing of the config_src
    #
    for disk in config.Disks:

        if disk == hd1:
            assert disk.Partitions is not None, """
The disk 'hd1' has no list of partitions.
"""
            assert len(disk.Partitions) == 2, """
Failed to properly assign partitions from config_src to disk 'hd1'.
""" + len(disk.Partitions) + """ partitions found, should be 2
"""
            assert (partition1 in disk.Partitions and
                    partition2 in disk.Partitions), """
Failed to find partition1 and/or partition2 in list of hd1 partitions
"""
        if disk == hd2:
            assert disk.Partitions is not None, """
The disk 'hd2' has no list of partitions.
"""
            assert len(disk.Partitions) == 2, """
Failed to properly assign partitions from config_src to disk 'hd2'.
""" + len(disk.Partitions) + """ partitions found, should be 2
"""
            assert (partition3 in disk.Partitions and
                    partition4 in disk.Partitions), """
Failed to find partition3 and/or partition4 in list of hd1 partitions
"""

    # todo przemyslec bad_config
    return True


