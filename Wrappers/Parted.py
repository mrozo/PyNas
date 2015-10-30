import subprocess
import re
from Wrappers.ShellCmdWrapper import ShellCmdWrapper

__author__ = 'm'

_RootPassword = 'k'

_PartedRegexp = {
    'PartedVersion': re.compile('GNU[ \t]+Parted[ \t]*([0-9\.]+)')
}


class PartedWrapper(ShellCmdWrapper):
    """
    Basic wrapper for gnu parted shell application
    """

    DevicePath = ""

    def __init__(self, device_path):
        self.DevicePath = device_path

    @staticmethod
    def get_disk_info(device_path):
        """
        Get and parse disk info using gnu parted
        :param device_path: device to be used
        :return: device info structure
        """
        parted_stdout = ShellCmdWrapper.execute_command(
            'parted',
            ['select ' + device_path, 'unit B', 'print', 'quit'],
            elevate_permissions=True
        )

        parted_stdout = parted_stdout[0]

        parted_version = ShellCmdWrapper.get_info_field(
            _PartedRegexp['PartedVersion'], parted_stdout
        )

        partitions = ShellCmdWrapper.parse_table(
            parted_stdout,
            ['Number', 'Start', 'End', 'Size', 'Type', 'File system',
             'Flags']
        )

        #
        # Process columns to make sure they are containing a proper type of
        # data, for numeric types strip the unit
        #
        for partition in partitions:
            partition['Number'] = int(partition['Number'])
            partition['Start'] = int(partition['Start'][0:-2])
            partition['End'] = int(partition['End'][0:-2])
            partition['Size'] = int(partition['Size'][0:-2])
            partition['Flags'] = partition['Flags'].strip().split(',')

        return {'PartedVersion': parted_version, 'Partitions':partitions}
